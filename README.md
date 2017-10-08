# RAM-JD
> 人生苦短，我用Python！

## 前言
做这个项目主要是因为我自己想买内存条了:crying_cat_face:，我那个辣鸡电脑内存还是4G，开个PS就卡成:dog:，AE做个小点的视频渲染就得好久。。。<br >
为了了解一下内存条的情况，于是一天晚上(2017.10.08)在图书馆闲来无事，把京东上的[内存条](https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&click=0)的数据按销量顺序全部爬下来了（说全部有点虚，总感觉漏掉了一些）

### 存到MySQL数据库的数据
<img src="https://i.loli.net/2017/10/08/59da21bd58882.png" alt="ScreenShots1.PNG" title="ScreenShots1.PNG" />

### 从MySQL导出为CSV
<img src="https://i.loli.net/2017/10/08/59da4562deb82.png" alt="ScreenShots4.PNG" title="ScreenShots4.PNG" />

## 爬取过程

这是京东搜索`笔记本内存条`并按销量排序的第一页的部分结果
<img src="https://i.loli.net/2017/10/08/59da20d37d4c1.png" alt="ram-jd" title="ram-jd"/>

本来是打算直接根据搜索出来的URL来爬数据，结果发现京东一页数据分两次加载，开始显示前30个商品，当滚动条下拉之后然后再异步加载后30个商品，于是这个方法只能作废了。

然后在翻页的时候发现了一些有趣的东西:trollface:

下面是第二页前30商品与某个[神秘的请求](https://search.jd.com/s_new.php?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page=3&s=61&click=0)(链接打开是404/request deny)
<img src="https://i.loli.net/2017/10/08/59da252a1dda3.png" alt="ScreenShots2.PNG" title="ScreenShots2.PNG" />
第二页后30商品与某个[神秘的请求](https://search.jd.com/s_new.php?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E5%86%85%E5%AD%98%E6%9D%A1&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&psort=3&page=4&s=91&scrolling=y&log_id=1507468392.71505&tpl=1_M&show_items=3233447,10127269543,10044385605,2529194,835000,10294709778,2352053,10294709775,11006859581,5159060,15502710963,11006859580,814822,2529192,2210077,1153806,14711288930,3420208,11262133881,2352059,3148016,1723166722,3039111,11034733327,3519237,10460276980,1630797125,1153804,10074571579,12746546253)
<img src="https://i.loli.net/2017/10/08/59da252a85b92.png" alt="ScreenShots3.PNG" title="ScreenShots3.PNG" />
切换到`Response`之后发现这两个请求返回的`HTML`中就包含了商品的各项数据，简单分析这两个链接的格式就能通用了。

## 分析
### 各店铺所占比例
**可以看到这六个店(`鼎信电脑办公专营店`、`联想400配件专卖店`、`瑞福德数码专营店`、`千诚致远专营店`、`悦智数码专营店`、`纽科旗舰店`)占了3/4+，或许我可以去这几个店买内存条。。。**
<img src="https://i.loli.net/2017/10/08/59da416cdc1e2.png" alt="shop_percent.png" title="shop_percent.png" />

### 商品名の词云
**`笔记本`、`内存条`、`DDR3`占比重大我能理解，但不是很懂`联想`(`Lenovo`)为啥占了这么大比重。然后可以看到大概现在主流的是4G和8G，16G和32G所占比重很小，在图中基本看不到:joy:**
<img src="https://i.loli.net/2017/10/08/59da42c33a18d.png" alt="cloud.png" title="cloud.png" />