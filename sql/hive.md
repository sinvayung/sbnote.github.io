#### 字符串函数

```sql
select split('pp,cc', ',')[0] as p, split('pp,cc', ',')[1] as c
select parse_url('http://m.qq.com/test/abc.html', 'HOST')
```

#### 类型转换

```sql
select conv('11', 16, 10)
select (cast('3' as int)&1) as a
```

#### 日期函数

```sql

```

#### 内存表创建

```sql
select explode(array('A','B','C')) as col1
select explode(map('A',10,'B',20,'C',30)) as (col1,col2)
select inline(array(struct('A',10,date '2015-01-01'),struct('B',20,date '2016-02-02'))) as (col1,col2,col3)
select stack(2,'A',10,timestamp '2015-01-01 18:30:01','B',20,timestamp '2016-01-01 18:30:01') as (col0,col1,col2)
```

#### 条件选择

```sql
select nvl(null, 100), nvl(200, 100), nvl("aaa", "bbb"),  nvl(null, "bbb")
select coalesce(null, '100', '200')
select case 2 when 1 then 100 when 2 then 200 when 3 then 300 else 0 end
select if(1=1, 100, 200), if(1==2,100,200)
```

#### 窗口函数

```sql
select t2.p, t2.c, t2.ds from (
    select t1.p, t1.c, t1.ds, rank() over (partition by p order by ds desc) as r from(
        select stack(3, 'MM', 'MMM1', 20200101, 'QQ', 'QQQ1', 20200103, 'QQ', 'QQQ2', 20200104) as (p, c, ds)
    ) t1
) t2
where t2.r=1
```



