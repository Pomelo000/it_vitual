一：1.底层：Mat类
Mat c0(5,5,CV_8C1,Scalar(4,5,6));     长，宽，数据类型，通道数 

2.range:截取
Mat f = Mat(e, Range(2, 4));

3.矩阵属性调用
核心函数：.cols (列), .rows (行), .step (行数×列数), .elemSize() (字节数), .total() (元素个数), .channels() (通道数)

五大基础类（必用） 
类名	用途	示例	说明
Mat​	图像/矩阵容器	Mat img = imread("1.jpg");	
Point​	二维坐标点	Point(100, 200)	像素位置、坐标
Size​	二维尺寸	Size(640, 480)	图片/区域大小
Rect​	矩形区域	Rect(100,100,200,300)	ROI提取、画框
Scalar​	颜色/数值	Scalar(255,0,0)	颜色值、参数


二：视频图像获取：
1.图片{
1.imread(string & 图片名,flags = 读取形式)

2.窗口可视化：
Namedwindow(窗口名称,窗口属性标志)

2显示窗口图片
Imshow()(窗口的名字，要显示的图像矩阵)  注意：如果没有先创建,会直接创建，flag为默认值）

3.保存
Imwrite(保存图像的 地址 与文件名,要保存的mat,保存图像需要的属性)
}

2.视频{
videoCapture(视频名称/摄像头id,参数)
Videowriter(地址文件名格式,编码器代码,fps,帧尺寸，是否彩色)
}
要一直显示图像，调用waitKey

三：降维与预处理
Range 识别特定区域

integral(gray_img, sum_img, sqsum_img);图像加速处理(原，标准求和，平方求和)

cvtColor（原图像，出图像，标志）
cvtColor(src, gray, COLOR_BGR2GRAY); // 变成单通道灰度图 (CV_8UC1)
cvtColor(src, hsv, COLOR_BGR2HSV);   // 变成三通道 HSV 图 (CV_8UC3)


滤波操作：
要去除椒盐噪声	中值滤波     blur(img, out_img, Size(5, 5));
求最大的去噪效果	均值滤波 + 大核
需要极高的计算速度	均值滤波   medianBlur(img, out_img, 5);
需要保留图像细节	双边滤波
高斯滤波          大尺寸     GaussianBlur(img, out_img, Size(5, 5), 0);

图像的分割:颜色分割或阈值分割
{
inRange（初图像，最大值，最小值，输出图像）
颜色分割

threshold(原始图像，输出图像，阈值，最大值（和第五个一起用），flag)
二值化
}

喂给yolo,归一化
src.convertTo(float_img, CV_32F, 1.0 / 255.0);

图像修补：腐蚀与膨胀
 Mat kernel = getStructuringElement(MORPH_ELLIPSE,Size(5,5));笔刷配置
morphologyEx(img, out_img, MORPH_OPEN, kernel);


四：特征提取：（转图像为数据）
1.边缘检测：

高阈值	低阈值	效果	适用场景
200	100	边缘稀疏，准确性高	需要高精度，容忍断裂
150	50	平衡性能（推荐）	通用场景
100	30	边缘丰富，可能含噪声	需要完整轮廓
80	25	细节丰富，噪声明显	纹理分析

Canny(binary_img, edges, 50, 150，算子直径);

HoughLinesP(edges, linesP, 1, CV_PI/180, threshold判定为直线的最低条件, minLineLength低于这个长度的线段直接不要, maxLineGap抗干扰);

findContours(image, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);转为计算机语言

转坐标：套外接图
Point2f center; // 用来接住输出的中心坐标
float radius;   // 用来接住输出的半径

// 把轮廓塞进去，瞬间得到圆心坐标和半径
minEnclosingCircle(valid_contours[0], center, radius);

cout << "圆心坐标: X=" << center.x << ", Y=" << center.y << endl;