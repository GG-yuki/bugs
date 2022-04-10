#!/usr/bin/python
from scipy.spatial.distance import pdist, squareform, euclidean
import numpy as np
import time

# Training Set S 
# Have M samples
# Divided into T class
# With N condition attributes.
# 
# Sample (from knn-data.txt):
# 0.17143108 0.15026921 0.21784143 -0.0894064 -0.09518636 -0.09099912 -0.05094884 0.00145187 -0.11828536 0.01082689 0.00461332 0.01170807 0.12530981 0.12763084 -0.06029766 0.19319022 -0.16994244 0.09382871 -0.0713816 -0.18627712 0.03397886 0.12139035 0.17584744 0.09011602 0.03947105 0.32759234 0.22752793 -0.15781775 0.18628438 0.04276126 -0.09016601 -0.02239298 -0.04248622 0.01329508 -0.23934488 -0.00449575 0.08784223 0.06845222 -0.03015003 0.12062091 0.19032593 0.0625155 0.02477192 -0.01028579 0.09869327 -0.17371099 -0.06272626 0.02261056 -0.20432729 -0.13255379 0.02452434 0.00411576 0.02888236 0.13303439 -0.04586671 0.0807283 0.22647177 -0.06402998 0.19440691 0.12054072 -0.01555257 0.07960476 0.03180799 -0.0134579 0.11603108 -0.0587856 0.15169829 -0.10895722 -0.00247767 -0.11142307 -0.07093495 -0.0672254 -0.01952415 0.05841121 0.23053604 0.01150951 0.08170953 0.2536397 -0.06402756 0.02087649 0.09436733 0.06605712 -0.22953287 0.07227629 0.00149115 -0.0440244 0.03446841 -0.03200138 -0.14209652 -0.05826599 0.08245 0.15154208 0.10126947 0.10923993 0.11463781 0.13879354 -0.27142203 -0.00717958 -0.14150417 -0.02699979 0.13917755 0.11837537 0.18428573 -0.07655263 -0.0921438 -0.07823294 -0.04577453 0.01398715 -0.10311522 -0.00376852 0.00364708 0.00799766 0.10547133 0.11222182 -0.04775156 0.1705032 -0.14286718 0.07788558 -0.05623695 -0.1605396 0.02888318 0.09935644 0.15010604 0.07603823 0.02423622 0.28661636 0.19678737 -0.1431032 0.15562026 0.03159494 -0.08549254 -0.02416303 -0.03737999 0.01101518 -0.20822282 -0.01786014 0.07010814 0.06118918 -0.02561868 0.10388313 0.15436563 0.04990598 0.02215378 -0.0010637 0.0649926 -0.14383242 -0.05144636 0.02212231 -0.17192604 -0.11706253 0.02354227 0.01148643 0.02912092 0.12127037 -0.0487974 0.07352068 0.19465405 -0.05063398 0.16696341 0.10200395 -0.00858924 0.07001011 0.03531862 -0.03359639 0.08343234 -0.07174771 0.12357353 -0.10008448 -0.00911572 -0.09134642 -0.06921568 -0.07293113 -0.0137085 0.05424437 0.19765733 0.01866256 0.05220041 0.21097232 -0.04837629 0.02029854 0.08940083 0.07201066 -0.18399945 0.05974483 0.00165744 -0.03900469 0.01998913 -0.0244367 -0.12216679 -0.04441646 0.06744681 0.13044587 0.09303664 0.08814421 0.10961656 0.11508407 -0.23956379 -0.00355534 -0.11811391 -0.01705651 0.17246729 0.14724962 0.22543953 -0.09396351 -0.10589773 -0.09453075 -0.06920269 0.02013744 -0.11670825 -0.00197191 0.00701753 0.01203702 0.12106562 0.13988781 -0.06377878 0.21609332 -0.16880515 0.10002808 -0.07350559 -0.19726881 0.0348421 0.12347987 0.17611295 0.09894745 0.01883216 0.35092545 0.24534419 -0.16797079 0.19049227 0.0393366 -0.10626041 -0.02349127 -0.03785237 0.02247183 -0.25596732 -0.01595355 0.09130406 0.07169626 -0.03630666 0.12932318 0.19502883 0.06746045 0.02203394 -0.00190845 0.0891166 -0.18391247 -0.05457155 0.02903355 -0.20780523 -0.15166305 0.02106848 0.00814268 0.03672159 0.14788228 -0.05230636 0.0982967 0.23662542 -0.05941983 0.20184506 0.1266218 -0.01240765 0.08362527 0.04179268 -0.03612465 0.11770107 -0.08338537 0.15628761 -0.11474695 -0.01564734 -0.10670209 -0.07859553 -0.07830718 -0.0147535 0.07800335 0.24313831 0.0218046 0.07442762 0.26722544 -0.05028531 0.02501493 0.10619087 0.09133738 -0.23014039 0.07401714 0.00322283 -0.03687645 0.02771911 -0.02733128 -0.15145814 -0.05236012 0.08884116 0.16385619 0.1126551 0.10342072 0.13463855 0.14832278 -0.28723016 -0.00504282 -0.14959459 -0.01649169 0.15558428 0.14038235 0.20672539 -0.08448551 -0.09584459 -0.08435255 -0.05320303 0.00963188 -0.11007517 0.00838997 0.00322189 0.01714753 0.10886094 0.11926559 -0.05619052 0.18350348 -0.15547068 0.08682913 -0.06565011 -0.17552194 0.03013964 0.10769153 0.16117652 0.08175527 0.03126686 0.30974257 0.21921651 -0.14881833 0.17338544 0.03580204 -0.08359807 -0.02118961 -0.03689981 0.00923355 -0.21836339 -0.00803611 0.08799982 0.06132304 -0.02526659 0.1161107 0.17196593 0.0566819 0.01319081 -0.00516264 0.09226988 -0.16310421 -0.06247139 0.03067413 -0.18960012 -0.13032499 0.02115129 0.00075195 0.02897047 0.12270314 -0.04867562 0.08431152 0.21028598 -0.05455381 0.1828848 0.11131394 -0.0182943 0.07599315 0.03637371 -0.01955842 0.1117444 -0.06022616 0.14349045 -0.10480284 -0.00222988 -0.09931791 -0.07237657 -0.06639774 -0.01519012 0.06298103 0.2154191 0.01428923 0.07092817 0.23725124 -0.05926299 0.02055393 0.08883255 0.07443087 -0.21478236 0.07109313 0.00118675 -0.03373353 0.02563123 -0.02316219 -0.13501181 -0.05085844 0.07881781 0.14118178 0.09464136 0.09918801 0.11555615 0.12699549 -0.2561391 0.00051517 -0.12902515 -0.02234022 13

# Input  : 	KNN training set S Have M samples
#			Several Z of increment set Have {M1, M2, ..., Mz} samples
# 
# Output :	KNN Model Set.

# KNN training set S :
# @param	x	training set  S
# @param	z 	Several of training sets Z

#def Cal_Class_Contribution(x):
	# Divided into T class in S
	# T = 0
	# label = 0~38; (Save them in Hash table, T = len(Hash table)) || (Save the Maximum Value in T)
	# if label > T:
	# 	T = label


	# m = len(x)
	# print 'len(x) = ' , m

# Read Data By File.
def Cal_Class_Contribution_By_File(data_file):
    # read data
    data = np.genfromtxt(data_file,  delimiter=" ", skip_header=False)

    class_hash_table = {}
    feature_hash_table = {}
    # n :the number of Condition attribute
    n_status = False
    for labels in data:

        # Calculate |t r|
        #           | ij|
        if n_status != True:
            # print 'labels -->', labels
            n = len(labels) - 1
            n_status = True

        # Calculate T
    	label = int(labels[-1])
    	if class_hash_table.has_key(label):
    		class_hash_table[label] += 1
    	else:
    		class_hash_table[label] = 1

        # Calculate |t  |
        #           | ij|
        # 
        # Input :
        # Sample +---------------+
        #        |1 0 5 8 class:5|
        #        |2 4 0 8 class:5|
        # Sample +---------------+
        #
        # Output:
        # {"class index"}
        # Sample {"5 0":2, "5 1":1, "5 2":1, "5 3":2}
        for i, feature in enumerate(labels[:-1]):
            if feature != 0:
                if feature_hash_table.has_key("{0} {1}".format(label, i)):
                    feature_hash_table["{0} {1}".format(label, i)] += 1
                else:
                    feature_hash_table["{0} {1}".format(label, i)] = 1


    
    print 'class_hash_table = ', class_hash_table

    # T     Done.
    T = len(class_hash_table.keys())
    print 'T = ', T

    # |t r| Done.
    # | ij|
    print 'n = ', n

    # |t  | Done.
    # | ij|
    #print 'feature_hash_table = ', feature_hash_table


    # use et_list +-------+ means Class Contribution Done.
    #             |0 --> n|
    #             ||      |
    #             |T      |
    #             +-------+
    et_list = [[0 for col in range(n+1)] for row in range(T)]
    
    class_arr = []
    for i in class_hash_table.keys():
        class_arr.append(i)

    for i in range(0,T):
        for j in range(0,n+1):
            if j == 0:
                et_list[i][j] = class_arr[i]
            else:
                autosum = 0
                for key2 in class_hash_table:
                    tij = feature_hash_table.get("{0} {1}".format(key2, j-1))
                    autosum += n / tij

                et_list[i][j] = -(autosum/T)

    return et_list,feature_hash_table


# Read Data By List.
def Cal_Class_Contribution_By_Data(data):

    class_hash_table = {}
    feature_hash_table = {}
    # n :the number of Condition attribute
    n_status = False
    for labels in data:

        # Calculate |t r|
        #           | ij|
        if n_status != True:
            # print 'labels -->', labels
            n = len(labels) - 1
            n_status = True

        # Calculate T
    	label = int(labels[-1])
    	if class_hash_table.has_key(label):
    		class_hash_table[label] += 1
    	else:
    		class_hash_table[label] = 1

        # Calculate |t  |
        #           | ij|
        # 
        # Input :
        # Sample +---------------+
        #        |1 0 5 8 class:5|
        #        |2 4 0 8 class:5|
        # Sample +---------------+
        #
        # Output:
        # {"class index"}
        # Sample {"5 0":2, "5 1":1, "5 2":1, "5 3":2}
        for i, feature in enumerate(labels[:-1]):
            if feature != 0:
                if feature_hash_table.has_key("{0} {1}".format(label, i)):
                    feature_hash_table["{0} {1}".format(label, i)] += 1
                else:
                    feature_hash_table["{0} {1}".format(label, i)] = 1


    
    print 'class_hash_table = ', class_hash_table

    # T     Done.
    T = len(class_hash_table.keys())
    print 'T = ', T

    # |t r| Done.
    # | ij|
    print 'n = ', n

    # |t  | Done.
    # | ij|
    #print 'feature_hash_table = ', feature_hash_table


    # use et_list +-------+ means Class Contribution Done.
    #             |0 --> n|
    #             ||      |
    #             |T      |
    #             +-------+
    et_list = [[0 for col in range(n+1)] for row in range(T)]
    
    class_arr = []
    for i in class_hash_table.keys():
        class_arr.append(i)

    for i in range(0,T):
        for j in range(0,n+1):
            if j == 0:
                et_list[i][j] = class_arr[i]
            else:
                autosum = 0
                for key2 in class_hash_table:
                    tij = feature_hash_table.get("{0} {1}".format(key2, j-1))
                    if isinstance(tij, int):
                        autosum += n / tij

                et_list[i][j] = -(autosum/T)

    return et_list,feature_hash_table
