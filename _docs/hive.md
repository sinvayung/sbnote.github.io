---
title: Getting Started
description: Getting started with Docsy Jekyll
---


### 字符串函数

```sql
select split('pp,cc', ',')[0] as p, split('pp,cc', ',')[1] as c
select parse_url('http://m.qq.com/test/abc.html', 'HOST')
```

### 类型转换

```sql
select conv('11', 16, 10)
select (cast('3' as int)&1) as a
```

### 日期函数

```sql
select 
    unix_timestamp(),  --当前时间, 如：1579923001
    unix_timestamp('2020-01-25 11:30:01'),  --如：1579923001
    unix_timestamp('2020-01-25 11:30:01', 'yyyy-MM-dd HH:mm:ss'),  --如：1579923001
    from_unixtime(1579060436),   --默认格式'yyyy-MM-dd HH:mm:ss'，如：2020-01-25 11:30:01
    from_unixtime(1579060436, 'yyyy-MM-dd HH:mm:ss'),  --如：2020-01-25 11:30:01
    year('2020-01-25 11:30:01'),  --如：2020
    month('2020-01-25 11:30:01'),  --如：3
    dayofmonth('2020-01-25 11:30:01'),  --如：25
    weekofyear('2020-01-25'),  --第几周，如：4
    pmod(datediff('2020-01-25 11:30:01', '1920-01-01') - 3, 7),  --周几
    date_add('2020-01-31', 1),  --后一天，如：2020-02-01
    date_sub('2020-01-01', 1),  --前一天，如: 2019-12-31
    datediff('2020-02-01', '2020-01-01'), --间隔几天，如：31
    date_sub(from_unixtime(unix_timestamp('20200125', 'yyyyMMdd'), 'yyyy-MM-dd'), 1),  --2020-01-24
    cast(from_unixtime(unix_timestamp('20200125', 'yyyyMMdd')-1*24*60*60, 'yyyyMMdd') as int)  --20200124
    
select date('2020-02-03'), timestamp('2020-02-03 18:01:02')
```

### 内存表创建

```sql
select explode(array('A','B','C')) as col1
select explode(map('A',10,'B',20,'C',30)) as (col1,col2)
select inline(array(struct('A',10,date '2015-01-01'),struct('B',20,date '2016-02-02'))) as (col1,col2,col3)
select stack(2,'A',10,timestamp '2015-01-01 18:30:01','B',20,timestamp '2016-01-01 18:30:01') as (col0,col1,col2)
```

### 条件选择

```sql
select nvl(null, 100), nvl(200, 100), nvl("aaa", "bbb"),  nvl(null, "bbb")
select coalesce(null, '100', '200')
select case 2 when 1 then 100 when 2 then 200 when 3 then 300 else 0 end
select if(1=1, 100, 200), if(1==2,100,200)
```

### 窗口函数

```sql
select t1.pkg, t1.uct, t1.ds, 
    rank() over (partition by pkg order by ds desc) as _rank,  --同一pkg下的序号(从1开始)
    count(uct) over (partition by pkg) as _count,   --同一pkg下, uct的个数
    sum(uct) over (partition by pkg) as _sum,   --同一pkg下, uct的总数
    lead(uct) over (partition by pkg order by ds) as _lead,   --同一pkg下, 当前的下一个uct
    lag(uct,1,0) over (partition by pkg order by ds) as _lag   --同一pkg下, 当前的上一个uct，若没有则默认0
    
from
(
    select stack(3, 'MM', 800, 20200101, 'QQ', 700, 20200101, 'QQ', 750, 20200102) as (pkg, uct, ds)
) t1
```

### 关联查询

##### Left Join

```sql
-- Left Join
select 
t1.app, t1.uct, t1.ds, t2.app, t2.category
from
(select stack(5, 'wechat', 800, 202001, 'wechat', 850, 202002, 'qq', 700, 202001, 'qq', 780, 202002, 'wesee', 180, 202001) as (app, uct, ds)) t1
left join
(select stack(3, 'wechat', 1, 'wesee', 2, 'xgame', 3) as (app, category)) t2
on t1.app=t2.app --and t1.uct<=800 -- and t2.category=1
-- where t2.app is null
-- where t2.category=1
-- where t2.app is null
-- where t2.app is not null

-- Note: on条件控制右边字段是否为null, 而左表字段都会返回
-- Note: 左表过滤条件放where中，右表过滤条件放on中或where中都可以(建议前者，效率快一点)
```

##### Left Semi Join

```sql
select 
 t1.app, t1.category --, t2.app, t2.uct, t2.ds
from
(select stack(3, 'wechat', 1, 'wesee', 2, 'xgame', 3) as (app, category)) t1
left semi join
(select stack(5, 'wechat', 800, 202001, 'wechat', 850, 202002, 'qq', 700, 202001, 'qq', 780, 202002, 'wesee', 180, 202001) as (app, uct, ds)) t2
on t1.app=t2.app 

-- left semi join 跟 inner join有类似，但也不同
-- left semi join会去重(左表对应多右表的时候), inner join不会
-- left semi join后，不能再where右边，因为右边字段已不存在 
```

##### Right Join

```sql
-- Right Join
select 
t1.app, t1.uct, t1.ds, t2.app, t2.category
from
(select stack(5, 'wechat', 800, 202001, 'wechat', 850, 202002, 'qq', 700, 202001, 'qq', 780, 202002, 'wesee', 180, 202001) as (app, uct, ds)) t1
right join
(select stack(3, 'wechat', 1, 'wesee', 2, 'xgame', 3) as (app, category)) t2
on t1.app=t2.app --and t2.category=1

-- Note: Right Join不要在on中加右边的过滤条件
```

##### Full Join

```sql
select 
t1.app, t1.uct, t1.ds, t2.app, t2.category
from
(select stack(5, 'wechat', 800, 202001, 'wechat', 850, 202002, 'qq', 700, 202001, 'qq', 780, 202002, 'wesee', 180, 202001) as (app, uct, ds)) t1
full join
(select stack(3, 'wechat', 1, 'wesee', 2, 'xgame', 3) as (app, category)) t2
on t1.app=t2.app --and t1.uct<=800 and t2.category=1

-- Note: Full Join不要加左表或右表的过滤条件
```

##### Inner Join 

```sql
select 
t1.app, t1.uct, t1.ds, t2.app, t2.category
from
(select stack(5, 'wechat', 800, 202001, 'wechat', 850, 202002, 'qq', 700, 202001, 'qq', 780, 202002, 'wesee', 180, 202001) as (app, uct, ds)) t1
inner join 
(select stack(3, 'wechat', 1, 'wesee', 2, 'xgame', 3) as (app, category)) t2
on t1.app=t2.app and t1.uct<=800 
```



