"¬
Ό

x 

conv1.weight 1Conv2D"Default/conv1-Conv2d**
pad_list    *
offset_a *
data_format:NCHW*
group*
output_names 
:output**
dilation*
mode*!
input_names :x:w*
kernel_size*
out_channel*
pad_mode	:valid*
pad *(
stride2




y

1 2ReLU"Default/relu-ReLU*
output_names 
:output*
input_names
 :x2






2 3MaxPool"Default/max_pool2d-MaxPool2d*
data_format:NCHW*
output_names 
:output*
input_names
 :x*
padding	:VALID*'
ksize*)
strides2




Ό

3 

conv2.weight 4Conv2D"Default/conv2-Conv2d**
pad_list    *
offset_a *
data_format:NCHW*
group*
output_names 
:output**
dilation*
mode*!
input_names :x:w*
kernel_size*
out_channel*
pad_mode	:valid*
pad *(
stride2






y

4 5ReLU"Default/relu-ReLU*
output_names 
:output*
input_names
 :x2








5 6MaxPool"Default/max_pool2d-MaxPool2d*
data_format:NCHW*
output_names 
:output*
input_names
 :x*
padding	:VALID*'
ksize*)
strides2






6 

cst1 7Reshape"Default/flatten-Flatten*
output_names 
:output**
input_names 
:tensor	:shape2	


γ

7 


fc1.weight 8MatMul"Default/fc3-Dense*
transpose_x1 *
output_names 
:output*
transpose_x2*#
input_names :x1:x2*
transpose_a *
transpose_b2

x
£

8 

fc1.bias 9BiasAdd"Default/fc3-Dense*
data_format:NCHW*!
input_names :x:b*
output_names 
:output2

x
r

9 10ReLU"Default/relu-ReLU*
output_names 
:output*
input_names
 :x2

x
ε

10 


fc2.weight 11MatMul"Default/fc3-Dense*
transpose_x1 *
output_names 
:output*
transpose_x2*#
input_names :x1:x2*
transpose_a *
transpose_b2

T
₯

11 

fc2.bias 12BiasAdd"Default/fc3-Dense*
data_format:NCHW*!
input_names :x:b*
output_names 
:output2

T
s

12 13ReLU"Default/relu-ReLU*
output_names 
:output*
input_names
 :x2

T
ε

13 


fc3.weight 14MatMul"Default/fc3-Dense*
transpose_x1 *
output_names 
:output*
transpose_x2*#
input_names :x1:x2*
transpose_a *
transpose_b2



₯

14 

fc3.bias 15BiasAdd"Default/fc3-Dense*
data_format:NCHW*!
input_names :x:b*
output_names 
:output2


38_37_1_construct
x


 
 
fc3.bias



fc3.weight


T
fc2.bias
T

fc2.weight
T
x
fc1.bias
x

fc1.weight	
x
(
conv2.weight



(
conv1.weight



"
15


*!
cst1?????????