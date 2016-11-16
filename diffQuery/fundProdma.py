#!/usr/bin/python
#-*-coding:utf-8-*-

import cx_Oracle as db
import os
import logging
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def queryOracle(sql):
    username = "prodma"
    passwd = "cfpttest"
    logging.info('prodma begin connect!')
    con = db.connect(username, passwd, "192.25.101.177:1521/afatest")
    logging.info('prodma connected!')
    cur = con.cursor()
    logging.info('prodma execute sql!')
    cur.execute(sql)
    logging.info('prodma executed !')
    result  = cur.fetchall()
    cur.close()
    con.close()
    return result


def getFundData():
    sql = '''
--公募基金
select bb.PRODUCT_NAME 产品名称,
bb.seccode 基金代码,
decode(IS_ETF, '0', '否', 1, '是', null) "是否是ETF",
decode(IS_LOF, '0', '否', 1, '是', null) "是否是LOF",
decode(IS_QDII, '0', '否', 1, '是', null) "是否是QDII",
decode(IS_BREAKEVEN, '0', '否', 1, '是', null) "是否保本型",
decode(IS_LEVEL, '0', '否', 1, '是', null) "产品是否分级",
GRADING_MECHANISM "分级份额占比",
to_char(substr(INVESTMENT_STRATEGY, 1, 50)) "投资策略",
manager_name "投资经理",
(select cc.display_value from v_dict_business cc where cc.column_name = 'MONEY_TYPE'and cc.value = nn.MONEY_TYPE) "交易币种",
to_char(substr(INVESTMENT_SCOPE, 1, 50)) "投资范围",
PERFORMANCE_BENCHMARK "业绩比较基准",
"管理费率",
"托管费率",
CUSTODIAN "托管人",
MIN_SUBSCRIBE_AMOUNT "最低认购金额（个人）" ,
(select count(*) from t_prod_fee f where f.product_id=bb.product_id and feedict_id in (1,2,3)) 费率数量,
( select count(aa.name) from xyzqproduct.T_PRODUCT_T_FUND_1272  aa
where aa.productcode=bb.product_code)投资经理数量
from t_prod_product bb,
t_prod_producttree mm,
t_Prod_Publicfund nn,
(select k.product_id,
max(decode(feedict_id, 4, k.charge_rate, null)) "管理费率",
max(decode(feedict_id, 5, k.charge_rate, null)) "托管费率"
from (select z.product_id,
z.feedict_id,
max(nvl(to_char(z.charge_rate, 'fm9999990.90') || '',
z.rateadded_explain)) charge_rate
from t_prod_fee_dict t, t_prod_fee z
where t.product_table_id = 11
and z.feedict_id = t.feedict_id
group by z.product_id, z.feedict_id) k
group by product_id) zz,(select count(*) fee_count,product_id from
t_Prod_Fee    aa where aa.feedict_id in(1,2,3)
group by product_id) zz1,(select count(*) hs_fee_count,product_id from
t_Prod_Fee    aa where aa.feedict_id in(1,2,3)
group by product_id) zz2,(
select to_char(wm_concat(aa1.name)) manager_name,productcode from xyzqproduct.T_PRODUCT_T_FUND_1272 aa1 where aa1.DimissionDate is null
group by aa1.productcode
        ) nn1
where bb.rec_status = 2
and mm.producttree_id = bb.product_table_id
and nn.product_id = bb.product_id
and nn.product_id = zz.product_id(+)
and nn.product_id = zz1.product_id(+)
and nn.product_id = zz2.product_id(+)
and bb.product_code = nn1.productcode(+)
order by (case
when bb.parent_id < 0 then
bb.product_id
else
bb.parent_id
end)'''
    result = queryOracle(sql)
    return result
    #for row in result:
    #    print "%s %s, %s, %s" % (row[0], row[1], row[2], row[3])
		   # print result
