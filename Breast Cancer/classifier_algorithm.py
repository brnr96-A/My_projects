
import numpy as np
import os
from pytictoc import TicToc
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import BernoulliNB
from mlxtend.plotting import plot_confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier




    

def RunMethods(Data,label,Train_data,Test_data,Train_lable,Test_lable,str_out,class_names):
    
        
    print(np.shape(Test_data))
    print(np.shape(Train_data))
    print(np.shape(Train_lable))
    print(np.shape(Test_lable))
  
    
    algorithms_name=['DT','KNN','MLP','NB','Hybrid']
    alg_num=len(algorithms_name)
    accuracy_array=np.zeros(alg_num)
    precision_array=np.zeros(alg_num)
    recall_array=np.zeros(alg_num)
    f1_score_array=np.zeros(alg_num)
    time_array=np.zeros(alg_num)

    t = TicToc()
    K=0;      
    print('---------------------DecisionTreeClassifier---------------------')
    t.tic() #Start timer
    classifier =DecisionTreeClassifier(max_depth=100, random_state=0)
    classifier.fit(Train_data, Train_lable)
    Test_predict = classifier.predict(Test_data)
    TimeKNN=t.tocvalue() #Time elapsed since t.tic()
    Con_matrix=confusion_matrix(Test_lable, Test_predict)
    classfi_report=classification_report(Test_lable, Test_predict,output_dict=True)
    
    fig, ax = plot_confusion_matrix(conf_mat=Con_matrix,
                                show_absolute=True,
                                show_normed=False,
                                colorbar=True)
    
    ax.set_title('confusion_matrix of DecisionTreeClassifier ')
    plt.show()  

    accuracy_array[K]=accuracy_score(Test_lable, Test_predict)
    precision_array[K]= classfi_report['macro avg']['precision'] 
    recall_array[K]= classfi_report['macro avg']['recall']    
    f1_score_array[K]= classfi_report['macro avg']['f1-score']
 
 
    
    
    time_array[K]=TimeKNN


    print('---------------------KNeighborsClassifier---------------------')
    K+=1;
    t.tic() #Start timer
    classifier = KNeighborsClassifier (n_neighbors=33)
    classifier.fit(Train_data, Train_lable)
    Test_predict = classifier.predict(Test_data)
    Con_matrix=confusion_matrix(Test_lable, Test_predict)
    TimeDT=t.tocvalue() #Time elapsed since t.tic()
    classfi_report=classification_report(Test_lable, Test_predict,output_dict=True)
    
    fig, ax = plot_confusion_matrix(conf_mat=Con_matrix,
                                show_absolute=True,
                                show_normed=False,
                                colorbar=True)
    
    ax.set_title('confusion_matrix of KNeighborsClassifier ')
    plt.show()  


        
    # save to array
    accuracy_array[K]=accuracy_score(Test_lable, Test_predict)
    precision_array[K]= classfi_report['macro avg']['precision'] 
    recall_array[K]= classfi_report['macro avg']['recall']    
    f1_score_array[K]= classfi_report['macro avg']['f1-score']
    time_array[K]=TimeDT






    print('---------------------MLPClassifier---------------------')
    K+=1;
    t.tic() #Start timer
    classifier= MLPClassifier(solver='lbfgs', alpha=1.e-05, random_state=40,hidden_layer_sizes=[100, 100], max_iter=1000)
    classifier.fit(Train_data, Train_lable)
    Test_predict = classifier.predict(Test_data)
    Timeclassifier_Boosting=t.tocvalue() #Time elapsed since t.tic()
    Con_matrix=confusion_matrix(Test_lable, Test_predict)
    classfi_report=classification_report(Test_lable, Test_predict,output_dict=True)
    
    fig, ax = plot_confusion_matrix(conf_mat=Con_matrix,
                                show_absolute=True,
                                show_normed=False,
                                colorbar=True)
    
    ax.set_title('confusion_matrix of MLPClassifier ')
    plt.show()



    
    # save to array
    accuracy_array[K]=accuracy_score(Test_lable, Test_predict)
    precision_array[K]= classfi_report['macro avg']['precision'] 
    recall_array[K]= classfi_report['macro avg']['recall']    
    f1_score_array[K]= classfi_report['macro avg']['f1-score']
    time_array[K]=Timeclassifier_Boosting
    
    
    print('--------------BernoulliNB----------------')
    K+=1;
    t.tic() #Start timer
    classifier =BernoulliNB()
    classifier.fit(Train_data, Train_lable)
    Test_predict = classifier.predict(Test_data)
    Timeclassifier_Bagging=t.tocvalue() #Time elapsed since t.tic()
    Con_matrix=confusion_matrix(Test_lable, Test_predict)
    classfi_report=classification_report(Test_lable, Test_predict,output_dict=True)
    
    fig, ax = plot_confusion_matrix(conf_mat=Con_matrix,
                                show_absolute=True,
                                show_normed=False,
                                colorbar=True)
    
    ax.set_title('confusion_matrix of BernoulliNB ')
    plt.show()  

    
    # save to array
    accuracy_array[K]=accuracy_score(Test_lable, Test_predict)
    precision_array[K]= classfi_report['macro avg']['precision'] 
    recall_array[K]= classfi_report['macro avg']['recall']    
    f1_score_array[K]= classfi_report['macro avg']['f1-score']
    time_array[K]=Timeclassifier_Bagging
    
    
    
    
    
    print('--------------VotingClassifier----------------')
    K+=1;
    t.tic() #Start timer
    clf1 = BernoulliNB()
    clf2 = KNeighborsClassifier(n_neighbors=3)
    clf3 = MLPClassifier(solver='lbfgs', alpha=1.e-05, random_state=1,hidden_layer_sizes=[10, 10], max_iter=1000)
    classifier = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft')
    classifier.fit(Train_data, Train_lable)
    Test_predict = classifier.predict(Test_data)
    TimeVoting_Classifier=t.tocvalue() #Time elapsed since t.tic()
    Con_matrix=confusion_matrix(Test_lable, Test_predict)
    classfi_report=classification_report(Test_lable, Test_predict,output_dict=True)
    
    fig, ax = plot_confusion_matrix(conf_mat=Con_matrix,
                                show_absolute=True,
                                show_normed=False,
                                colorbar=True)
    
    ax.set_title('confusion_matrix of VotingClassifier ')
    plt.show()  

    #plot_RFE(classifier,Data,label,2)
    
    # save to array
    accuracy_array[K]=accuracy_score(Test_lable, Test_predict)
    precision_array[K]= classfi_report['macro avg']['precision'] 
    recall_array[K]= classfi_report['macro avg']['recall']    
    f1_score_array[K]= classfi_report['macro avg']['f1-score']
    time_array[K]=TimeVoting_Classifier   
    
    
    
    
    

    
    
    print('--------------------result--------------------------')
    fig1=plt.figure(figsize=(6, 7)) #  
    plt.bar(algorithms_name, accuracy_array,color = ['red', 'green'])
    plt.xticks(algorithms_name, rotation=70)
    plt.ylabel('percent%')
    plt.title('Accuracy of all Algorithm')
    plt.xlabel("Algoritm names")
    for i, v in enumerate(accuracy_array):
        v=round(v,2)
        plt.text(i-0.2 , v+0.01 , str(v), color='blue', fontweight='bold')
    fig1.show()
    plt.savefig(os.path.join(str_out+' accuracy.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
    
     
    fig2=plt.figure(2) #  
    plt.bar(algorithms_name, precision_array,color = ['red', 'green'])
    plt.xticks(algorithms_name, rotation=70)
    plt.ylabel('percent%')
    plt.title('Precision of all Algorithm')
    plt.xlabel("Algoritm names")
    for i, v in enumerate(precision_array):
        v=round(v,2)
        plt.text(i-0.2 , v+0.01 , str(v), color='blue', fontweight='bold')
    fig2.show()
    plt.savefig(os.path.join(str_out+' precision.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
    
    
    
    
    fig3=plt.figure(3) #  
    plt.bar(algorithms_name, recall_array,color = ['red', 'green'])
    plt.xticks(algorithms_name, rotation=70)
    plt.ylabel('percent%')
    plt.title('Recallof all Algorithm')
    plt.xlabel("Algoritm names")
    for i, v in enumerate(recall_array):
        v=round(v,2)
        plt.text(i-0.2 , v+0.01 , str(v), color='blue', fontweight='bold')
    fig3.show()
    plt.savefig(os.path.join(str_out+' recall.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
    
    
    
    fig4=plt.figure(4) #  
    plt.bar(algorithms_name, f1_score_array,color = ['red', 'green'])
    plt.xticks(algorithms_name, rotation=70)
    plt.ylabel('percent%')
    plt.title('f1-score of all Algorithm')
    plt.xlabel("Algoritm names")
    for i, v in enumerate(f1_score_array):
        v=round(v,2)
        plt.text(i-0.2 , v+0.01 , str(v), color='blue', fontweight='bold')
    fig4.show()
    plt.savefig(os.path.join(str_out+' f1_score.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
    
    
    
    fig5=plt.figure(figsize=(10, 8)) # 
    plt.bar(algorithms_name, time_array,color = ['blue', 'green'])
    plt.xticks(algorithms_name, rotation=70)
    plt.ylabel('time(s)')
    plt.title('time of all Algorithm')
    plt.xlabel("Algoritm names")
    for i, v in enumerate(time_array):
        v=round(v,2)
        plt.text(i-0.2 , v+0.01 , str(v), color='blue', fontweight='bold')
    plt.savefig(os.path.join(str_out+' time.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
    fig5.show()
    
    
    np.savetxt(str_out+'accuracy.csv', accuracy_array, delimiter=',')
    np.savetxt(str_out+' precision_array.csv', precision_array, delimiter=',')
    np.savetxt(str_out+'recall_array.csv', recall_array, delimiter=',')
    np.savetxt(str_out+' time_array.csv', time_array, delimiter=',')
    np.savetxt(str_out+' f1-score.csv', f1_score_array, delimiter=',')

 