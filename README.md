# GoPansa
### Image-based meat grade automatic measurement service

<h3 align="center">Our Icon</h3>
<p align="center">
  <img src="./images/our_icon.png" width="30%" title="logo" ></img>
</p><br>

## π¨βπ¦βπ¦ Members 
- [Minku Koo](https://github.com/Minku-Koo) &nbsp;/&nbsp; *corleone@kakao.com*
- [Jiyong Park](https://github.com/Ji-yong219) &nbsp;/&nbsp; *wldydslapjyy@naver.com*
- [Heebeom Yang](https://github.com/takeny1998) &nbsp;/&nbsp; *takeny1998@gmail.com*
- [Hyunmoo Lee](https://github.com/Im-flying-sparrow) &nbsp;/&nbsp; *hm11l1@naver.com*

## π Table of Contents
- [Members](#-members)
- [DataSet](#-dataset)    
- [Deep Learning Model Performance](#-deep-learning-model-performance)
- [WBS](#-wbs)
- [User Interface](#-user-interface)
- [Testing Video](#-testing-video)
- [SW Architecture](#-sw-architecture)
- [Award](#-award)
- [Articles](#-articles)

## πΎ DataSet
#### We get data from [AI HUB : μΆμ°λ¬Ό νμ§(QC) μ΄λ―Έμ§](https://aihub.or.kr/aidata/30733)
### πΏ Sample Data
**Cow (Grade 1++, 1+) : 60,000 μ₯**
<p align="">
  <img src="./sample_data/QC_cow_segmentation_1++_022909.jpg" width="20%" title="cow1++" ></img>
  <img src="./sample_data/QC_cow_segmentation_1+_054780.jpg" width="20%" title="cow1+" ></img>
</p>

**Pig (Grade 1+, 1) : 10,000 μ₯**
<p align="">
  <img src="./sample_data/QC_pig_segmentation_1+_005015.jpg" width="15%" title="pig1+" ></img>
  <img src="./sample_data/QC_pig_segmentation_1_006635.jpg" width="15%" title="pig1" ></img>
</p>

## π Deep Learning Model Performance
+ ### Using ResNext Model
+ ### Transfer Learning through Fine Tuning

**π Train Accuracy (Cow, Pig)**
<p align="">
  <img src="./deeplearning_model/performance_graph/cow_acc.png" width="30%" title="cow_acc" ></img>
  <img src="./deeplearning_model/performance_graph/pig_acc.png" width="30%" title="pig_acc" ></img>
</p>

**π Train Loss (Cow, Pig)**
<p align="">
  <img src="./deeplearning_model/performance_graph/cow_loss.png" width="30%" title="cow_loss" ></img>
  <img src="./deeplearning_model/performance_graph/pig_loss.png" width="30%" title="pig_loss" ></img>
</p>


## π  WBS
<p align="center">
  <img src="./images/GoPansa_WBS_black.png" width="80%" title="wbs" ></img>
</p><br>

## π₯ User Interface

### Index Page
<p align="">
  <img src="./UI/index.png" width="70%" title="index" ></img>
</p><br>

### Register Profile & Store
<p align="">
  <img src="./UI/register.png" width="40%" title="register" ></img>
  <img src="./UI/register_store.png" width="40%" title="register_store" ></img>
</p><br>

### MyPage & Payment
<p align="">
  <img src="./UI/mypage.png" width="40%" title="mypage" ></img>
  <img src="./UI/payment.png" width="40%" title="payment" ></img>
</p><br>

### Check Meat Grade (Cow)
<p align="">
  <img src="./UI/check_cow_input.png" width="40%" title="check_cow_input" ></img>
  <img src="./UI/check_cow.png" width="40%" title="check_cow" ></img>
</p><br>

### Show Meat Grade Table (Cow & Pig)
<p align="">
  <img src="./UI/cow_grade_taeble.png" width="40%" title="cow_grade_taeble" ></img>
  <img src="./UI/pig_grade_taeble.png" width="40%" title="pig_grade_taeble" ></img>
</p><br>

### Map
<p align="">
  <img src="./UI/map.png" width="50%" title="map" ></img>
</p><br>

## π½ Testing Video
### You can see the Testing Video [here](https://www.youtube.com/watch?v=VUpD5PQ4sMU) (Youtube)


## β SW Architecture
<p align="center">
  <img src="./images/SW_structure.png" width="40%" title="sw_structure" ></img>
</p><br>

## π Award
### 2021λ μ  2ν μΆ©λΆ κ³΅κ³΅λ°μ΄ν°νμ© μ°½μκ²½μ§λν μ΅μ°μμ μμ
<p align="center">
  <img src="./images/Poster_2021.jpg" width="35%" title="poster" ></img>
</p><br>

## π° Articles

- [μΆ©λΆκ³ΌκΈ°μ, κ³΅κ³΅λ°μ΄ν° νμ© μ°½μκ²½μ§λν λ³Έμ  2κ°ν μ§μΆ](https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=001&oid=030&aid=0002963578)
- [μ²­μ£Όλ, κ³΅κ³΅λ°μ΄ν° μ°½μκ²½μ§λν μ΅μ°μμ](http://www.kyosu.net/news/articleView.html?idxno=74608)
- [μ²­μ£Όλ, κ³ κΈ° μ¬μ§λ§μΌλ‘ μ‘μ§ λ±κΈ μΈ‘μ  κ°λ₯ βμ±β κ°λ°](http://cc.newdaily.co.kr/site/data/html/2021/08/23/2021082300146.html)
- [μΆ©λΆλ-μΆ©λΆκ³ΌκΈ°μ 'κ³΅κ³΅λ°μ΄ν° νμ© κ²½μ§λν μμμ κ°μ΅'](https://thesegye.com/news/newsview.php?ncode=1065613402569021)
