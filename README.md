## 京东内存条数据分析:full_moon:
> 人生苦短，我用Python！

## 声明
> 本项目所有数据来自 **京东**, 获取与共享之行为或有侵犯 **京东** 权益的嫌疑, 若被告知需停止共享与使用, 本人会及时删除整个项目. 请您了解相关情况, 并遵守  **京东** 协议。

## 前言
做这个项目主要是因为我自己想买内存条了:crying_cat_face:，我那个辣鸡电脑内存还是4G，开个PS就卡成:dog:，AE做个小点的视频渲染就得好久。。。<br >
为了了解一下内存条的情况，于是一天晚上(2017.10.08)在图书馆闲来无事，把京东上的[内存条](https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&click=0)的数据按销量顺序全部爬下来了（说全部有点虚，总感觉漏掉了一些）

## 爬到的数据
~~仅爬了按销量排行的 41 页数据, 共得到 **2460** 条数据.~~

双十一之后更新(17/11/20), 爬了按销量排行的 48 页数据, 共得到 **2879** 条数据. 分析图没有修改, 工程量有点大(其实是懒), 多加了一些基于数据的分析.

![ram-1](https://github.com/LewisTian/RAM-JD/blob/master/images/ram-1.png)

### 存到MySQL数据库的数据
<img src="https://i.loli.net/2017/10/08/59da21bd58882.png" alt="ScreenShots1.PNG" title="ScreenShots1.PNG" />

### 从MySQL导出为CSV
<img src="https://i.loli.net/2017/10/08/59da4562deb82.png" alt="ScreenShots4.PNG" title="ScreenShots4.PNG" />

## 爬取过程

这是京东搜索`笔记本内存条`并按销量排序的第一页的部分结果

<img src="https://i.loli.net/2017/10/08/59da20d37d4c1.png" alt="ram-jd" title="ram-jd"/>

本来是打算直接根据搜索并排序之后的[URL](https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&psort=3&click=0)来爬数据，结果发现京东一页数据分两次加载，开始显示前30个商品，当滚动条下拉之后然后再异步加载后30个商品，于是这个方法只能作废了。

天无绝人之路，当我在翻页的时候发现了一些有趣的东西:trollface:

下面是第二页前30个商品与某个[神秘的请求](https://search.jd.com/s_new.php?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page=3&s=61&click=0)(链接打开是404/request deny)

<img src="https://i.loli.net/2017/10/08/59da252a1dda3.png" alt="ScreenShots2.PNG" title="ScreenShots2.PNG" />

第二页后30个商品与某个[神秘的请求](https://search.jd.com/s_new.php?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page=4&s=91&scrolling=y&log_id=1507468392.71505&tpl=1_M&show_items=3233447,10127269543,10044385605,2529194,835000,10294709778,2352053,10294709775,11006859581,5159060,15502710963,11006859580,814822,2529192,2210077,1153806,14711288930,3420208,11262133881,2352059,3148016,1723166722,3039111,11034733327,3519237,10460276980,1630797125,1153804,10074571579,12746546253)

<img src="https://i.loli.net/2017/10/08/59da252a85b92.png" alt="ScreenShots3.PNG" title="ScreenShots3.PNG" />

切换到`Response`之后发现这两个请求返回的`HTML`中就包含了商品的各项数据（名称、店铺、价格等等），简单分析这两个链接的格式就能通用了，excited！接下来就简单了，脚本细节就不多赘述了。

<img src="https://pic4.zhimg.com/50/333412b786c353dc5a761aa7ed3bf75b_hd.jpg" alt="excited.jpg" title="excited.jpg" />


## 结果分析
### 全部分析图请见 [ECharts](https://lewistian.github.io/RAM-JD/)
### 各店铺所占比例
**可以看到这六个店(`鼎信电脑办公专营店`、`联想400配件专卖店`、`瑞福德数码专营店`、`千诚致远专营店`、`悦智数码专营店`、`纽科旗舰店`)占了3/4+，尤其是第一个`鼎信电脑办公专营店`有725条数据，占了1/4+，简直可怕。`金士顿官方旗舰店`在第九，也是不错了**

<img src="https://i.loli.net/2017/10/08/59da416cdc1e2.png" alt="shop_percent.png" title="shop_percent.png" />

### 商品名の词云
- 生成词云代码可参考项目[WordCloud](https://github.com/LewisTian/WordCloud)

**`笔记本`、`内存条`、`DDR3`占比重大我能理解，但不是很懂`联想`(`Lenovo`)为啥占了这么大比重。然后可以看到大概现在主流的是4G和8G（其实我也打算买个8G的），16G和32G所占比重很小，在图中基本看不到:joy:**

<img src="https://i.loli.net/2017/10/08/59da42c33a18d.png" alt="cloud.png" title="cloud.png" />

### 不同容量内存条所占比例
果然买的最多还是8G和4G

<img src="https://i.loli.net/2017/10/09/59dafae4852be.png" alt="ScreenShots5.png" title="ScreenShots5.png" width="500" />

### 不同价格区间商品数
还是300-400这一区间的内存条比较火啊

<img src="https://i.loli.net/2017/10/09/59db5431247a1.png" alt="ScreenShots7.png" title="ScreenShots7.png" />

*17/11/20更新*
### 价格最高/最低的10件内存条
看着这价格, 我也只能看看...
![ram-2](https://github.com/LewisTian/RAM-JD/blob/master/images/ram-2.png)
上面贵的吓死人, 但下面这也太便宜了吧, 怕不是假的内存条的吧
![ram-3](https://github.com/LewisTian/RAM-JD/blob/master/images/ram-3.png)

### 评论最高的10件内存条
好巧哇, 我买的好像就是下面第一个内存条哇...
![ram-4](https://github.com/LewisTian/RAM-JD/blob/master/images/ram-4.png)

## 使用说明
首先把仓库克隆到本地然后安装所有用到的库
```
>> git clone https://github.com/LewisTian/RAM-JD.git
>> cd RAM-JD
>> pip install -r requirements.txt
```
由于将爬到的数据保存到 [MySQL](https://www.mysql.com/) 数据库, 请先安装好待用. (我安装的版本是5.7)

然后修改 `ram.py` 中链接 MySQL 数据库的若干变量（`$user` `$psw` `$db`），新建 `ram` 表用来存储数据，可参考下面建表语句
```
CREATE TABLE ram(
   id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(255),
   price VARCHAR(45),
   shop VARCHAR(45),
   comments VARCHAR(45),
   href VARCHAR(45));
```

如果前面没有问题运行脚本就可以了
```    
>> python ram.py
```
最后登录 MySQL 数据库查看数据是否保存成功
```
>> mysql -u $user -p
mysql> use $db;
mysql> select count(*) from ram;
```
导出数据为CSV
```
SELECT * FROM ram INTO OUTFILE '$path/ram.csv' 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '/r/n';
```
**注意，上面 `$path` 为 MySQL 的配置文件 `my.ini` 中 `secure-file-priv` 的路径，否则应该会报这个错误**
`ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement`

## LICENSE
[MIT](https://github.com/LewisTian/RAM-JD/blob/master/LICENSE)
