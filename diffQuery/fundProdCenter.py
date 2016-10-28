#!/usr/bin/python
#-*-coding:utf-8-*-

import cx_Oracle as db
import os
import logging
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
logging.basicConfig(level=logging.INFO)

def queryOracle1(sql):
    username = "ljit"
    passwd = "ljit"
    logging.info('prodCenter begin connect! username=' + username + ' passwd=' + passwd)
    con = db.connect(username, passwd, "129.20.13.81:1521/orcl")
    logging.info('prodCenter connected!')
    cur = con.cursor()
    logging.info('prodCenter begin execute sql!')
    cur.execute(sql)
    logging.info('prodCenter executed!')
    result  = cur.fetchall()
    cur.close()
    con.close()
    return result


def getFundData():
    sql = '''
with a as (
select s.f2_1090,s.f16_1090,s.ob_object_name_1090,wm_concat(t.f2_1272) f2_1272 from xyzqproduct.tb_object_1090 s left join
xyzqproduct.tb_object_1272 t on s.f2_1090=t.f1_1272
where s.f4_1090='J' and s.f19_1090='0'
group by s.f2_1090,s.f16_1090,s.ob_object_name_1090
union
select s.f1_0014,s.f3_0014,s.f4_0014,wm_concat(t.f2_1272) f2_1272 from xyzqproduct.tb_object_0014 s left join
xyzqproduct.tb_object_1272 t on s.f1_0014=t.f1_1272
where s.f5_0014=1 and s.f2_0014='111002000'
group by s.f1_0014,s.f3_0014,s.f4_0014
),
 c as (
         select t.f1_1099,t.ob_object_name_1099,t.f68_1099,t.f28_1099,t.f29_1099,t3.ob_object_name tg,
         t.f17_1099,t.f102_1099,
         t4.ob_object_name tradecode,
         (case when s1.f6_1400=1 then '是' else '否' end) isetf,
         (case when s2.f6_1400=1 then '是' else '否' end) islof,
         (case when s3.f6_1400=1 then '是' else '否' end) isqdii,
         (case when s4.f6_1400=1 then '是' else '否' end) isbaoben,
         (case when B.shuliang>1 then '是' else '否' end) isfenji,
         t1.f4_1967 fenjizhanbi
          from xyzqproduct.tb_object_1099 t
          left join xyzqproduct.tb_object_1967 t1 on t.f1_1099=t1.f2_1967
          left join xyzqproduct.tb_object_1090 t2 on t.f1_1099=t2.f2_1090
          left join xyzqproduct.t_product_t_pub_1018 t3 on t3.comcode=t.f13_1099
          left join xyfindb.t_pub_1023 t4 on t4.currencycode=t2.f23_1090
          left join xyzqproduct.tb_object_1400 s1 on t.f1_1099=s1.f2_1400 and s1.f3_1400='2001020200'
          left join xyzqproduct.tb_object_1400 s2 on t.f1_1099=s2.f2_1400 and s2.f3_1400='2001020300'
          left join xyzqproduct.tb_object_1400 s3 on t.f1_1099=s3.f2_1400 and s3.f3_1400 like '20010108%'
          left join xyzqproduct.tb_object_1400 s4 on t.f1_1099=s4.f2_1400 and s4.f3_1400='2001020x00'
          left join (select ob_object_name_1099,count(*) shuliang from xyzqproduct.tb_object_1099
                   group by ob_object_name_1099) B on B.ob_object_name_1099=t.ob_object_name_1099
           where t2.f19_1090=0
           ),
            d as (
                    select t.f1_1099,s2.name from xyzqproduct.tb_object_1099 t
                    left join xyzqproduct.tb_object_1400 s on t.f1_1099=s.f2_1400
                    left join xyzqproduct.tb_object_1022 s2 on s.f3_1400=substr(s2.code,1,10)
                    where s.f3_1400 like '2003%'
                    and s2.levelnum=5 and (s.f5_1400>=t.f23_1099 or s.f6_1400=1)
                    )
            select c.ob_object_name_1099 产品名称,a.f16_1090 基金代码,c.isetf 是否ETF,c.islof 是否LOF,c.isqdii 是否QDII,c.isbaoben 是否保本,c.isfenji 是否分级,c.fenjizhanbi 分级占比,
            d.name 投资策略,a.f2_1272 投资经理,c.tradecode 交易币种,c.f17_1099 投资范围,c.f102_1099 业绩比较基准,c.f28_1099 管理费率,c.f29_1099 托管费率,
            c.tg 托管公司,'' 最低定投金额
            from a
            inner join c on a.f2_1090=c.f1_1099
            inner join d on a.f2_1090=d.f1_1099
            order by a.f16_1090
    '''
    result = queryOracle1(sql)
    return result
        # print result
