#!/usr/bin/env python
# coding: utf-8

# # Analysing youtube channel statistics in 2017 in France

# I will work on:
# - Reading the data, and overview its structure,
# - Sorting dataframe,
# - Correlation between number of views and number of comments,
# - The frequency of tags in popular videos (with the use of regular expressions),
# - Grouping dataframe according to youtube channels. 

# ## Reading the data, and overview its structure

# The first step to work with data is to import it as a framework using pandas. Since the corresponding data is registered in csv (comma separated values) format, I read the data using method **read_csv**. The output of read_csv() method is a dataframe, which in the following peice of code it is referred to as data variable.

# In[1]:


import pandas as pd

data = pd.read_csv('FRvideos.csv')


# There are some useful features in pandas to take a look at a data frame. The method **head()** is one of them that as an argument accepts the number of rows to be desplayed from the top of the dataframe. In below, I illustrate the first 15 lines of the dataframe.

# In[2]:


data.head(15)


# In the same way, the method tail can be used to take a look at the bottom lines of the dataframe. The same as head, it is possible to pass an argument to specify the number of lines to be shown. If I pass the argument 15 to the method tail, it depicts the last fifteen lines of the data frame.

# In[3]:


data.tail(15)


# Another important features that give a nice overview of the data frame are the attribute **shape** and the method **info( )**. The shape attribute returns the dimensions of the data frame:

# In[4]:


data.shape


# In this example, the data frame (indicated by data) consists of 40724 rows and 16 colums. Method **info( )** gives some more specific information about the type of data in data frame as well as its dimension. 

# In[5]:


data.info()


# The method **info( )** for the dataframe **data** displays the 16 columns, the number of values which are not null, and the type of objects as **Dtype** . Speaking of which, the more frequent data types or dtype in pandas are objects (including strings), int64(to represent integer values), float64(to represent foalt values), and bool which is used for boolean values. Another important feature to access the names of columns in the dataframe and to manipulate them is the attribute columns. I will use it in the feature to manipulate the column names. In the following this attribute is used to extract the column names of the data frame data.

# In[7]:


data.columns


# ## Sorting data framea (analysing the popularity of videos in the dataframe.)

# As it is mentioned above, there are some interesting columns that can be used to analyse the videos. I know that youtube uses the number of comments for a video as a parameter to rank the videos. So, let's take a look at it and see what we can get from it. The corresponding column is **'comment_count'**, with data type as int64. So, the first thing that I can check is to find out which videos have the higher number of comments. One way to do that is to sort the values based on values of the corresponding column. The method **sort_values** is for that purpose. it sorts the dataframe based on the values of the columns that are listed in the feature **by**. In the following, I have used the method to sort the data frame based on the values of column **comment_count**. Now, note that by default the method **sort_values**, sort the values in a data frame in ascending order.

# In[6]:


data.sort_values(by = ['comment_count'])


# As it is shown in the sorted data frame, the last video is the one with the most number of comments. This video has gotten 1040912 comments and the video is titled by BTS(probably some chinese words) FAKE LOVE. 
# 
# 
# Now, by assigning value ```False```to the **ascending** attribute of the method **sort_values**, I can reverse the sorting order. Note that by default its value is ```True```, which corresponds to sorting dataframe by ascending order of specified values.

# In[9]:


data.sort_values(by = ['comment_count'], ascending = False)


# Note that **sort_values** is not an inplace method, which means using it on the dataframe does not change the ordering of values in the main dataframe. There is a very good reason for that: since in pandas we deal with large data frames if most of methods were "in place methods", many unexpeted errors can happen. However, in pandas we can first see the effect of a method on data frame and then if it was what we want we can save it. In my example. I save the results by assigning it to another dataframe (sorted_data).

# In[7]:


sorted_data = data.sort_values(by=['comment_count'], ascending = False)


# In[8]:


sorted_data

Another interesting method that can be used is **nlargest( )** method. As its name suggests, it returns the largest values in a dataframe. It accepts two arguments. The first one is the number of rows to be shown and the second one refers to the column according to which the largest values are chosen. In the following the method is used to get the 10 largest comment_count values as well as other values corresponding to them in the data frame.
# In[9]:


data.nlargest(10,'comment_count')


# Now imagine a situation that there are two videos with the same number of comments. In this case, values of other columns can play the role of a tie breaker. For instance, if the number of comments for two videos "A" and "B" are the same, we want to refer to the values in the column **likes** and rank the video higher if it has a higher number of likes.

# In[13]:


data.sort_values(by=['comment_count','likes'], ascending = False)


# Since in our dataframe there may not be a case that two videos have the same number of comments, there is not really need to check the values of **likes** column. But there are situations that using more than one column to sort a dataframe is inevitable.

# In a still different scenario, imagine a case that we want to sort data frame based on the the number of comments for videos in descending order, but tie happens we want to sort videos based on an ascending order of values in the **dislike** column. To do that, we can pass a list of boolean values to the **ascending** parameter, such that each value of it corresponds to a column in the list of columns.

# In[14]:


data.sort_values(by=['comment_count','dislikes'], ascending = [False, True])


# Again, in our dataframe it does not make a big difference since it is rarely possible that two videos have the same number of comments.

# Now let's say, we want to verify which and how many times a youtube channel have made the most popular youtube videos. Let's say for me the popular videos are fifty videos with the most number of comments:

# In[12]:


most_popular_videos = data.nlargest(50, 'comment_count')
most_popular_videos


# In[13]:



channels = most_popular_videos['channel_title']
channels


# Normally, histograms are the best choice to visualize the number of times that specific things happen in a given set of data, however, It seems to me that the **bars** can be an appropriate choice to represent the frequency of youtube channels in this example. There are two reasons for that. The first reason is that histogram is normally used to count the frequency in interals while, in this example, there is no internals, and we need frequency of unique values(youtube channels). The second reason is that I can easily extract the frequency of values used in a pandas series (dataframe columns) using the method **value_counts** . 

# In[14]:


frequency = channels.value_counts()
frequency


# For making bars, the other thing that I need is the name of the youtube channels that published the most popular videos. I can get them easily using the **unique** method, which returns each value in a pandas Series (column of data frame) just once.

# In[15]:


names = channels.unique()
names


# To do the plot, I first import the pyplot from matplotlib and use **barh** to make a horizontal bar. The reason to use barh and not bar is that the youtube names are big and if I use bar, they will overlap each other, which makes it hard to read the labels. Of course, there are mathods to rotate the labels of the x-axis and avoind overlapping but still it is not easy to read the vertical youtube names!

# In[16]:


from matplotlib import pyplot as plt
plt.barh(names,frequency)
plt.xlabel('Number of videos published by the channel in 50 most hits')
plt.ylabel('Name of top youtube channels')
plt.show()


# ## Correlation between the number of views and number of comments

# In the previous section, we have considered videos with more comments as "popular ones". Let's assume the popularity of a video is considered based on the number of likes that it has, and I want to analyse the behavior of viewers in commenting a video. I will do this analyse by calculating the percentage of comments for a video. 

# To do this, I am going to use the two columns **views** and **comment_count** to create a new column for the percentage. Adding a new column to a dataframe is as simple as choosing a name for it, and assign some values to it. Let's name the new column as **view_comment_percentage**, so I calculate the percentage value for each row of dataframe as below: 

# In[17]:


data['view_count_percentage'] = (data['comment_count']/ data['views'])*100


# In[18]:


data


# As it is given in the last column of the framework, it seems that for many of the videos, around one percent of viewers leave a comment. Let's see how these numbers vary for the 20 most (like-based) popular videos.

# Now, it seems to me that referring to the last column name is a little hard, since its name is big and it is difficult to remember it. So I am going to change the name to something much smaller like **VCP** which stands for views comment count percentage. To do that I use the method **rename** and the attribute **columns** as below.

# In[25]:


data.rename(columns={'view_count_percentage':'VCP'} , inplace = True)
data


# Note that the attribute **inplace** is a common attribute in many of the  methods that manipulate dataframes, and the pilosophy behind that is to avoid unwanted changes in dataframes, and so to avoid errors.

# Since the dataframe has changed a little bit so far, I am again going to extract the twenty rows with the largest numbers of comment.

# In[26]:


most_popular_videos = data.nlargest(20,'likes')


# In[27]:


most_popular_videos


# Based on the values of **VCP** column, it seems that the percentage of viewers who commented a video somehow corresponds to the popularity of the video, which is logical to me. To validate it, I am going to compare this percentage to the same value for the third 20 most popular videos.

# To find these values, one way is to first sort the dataframe in descending order, and to select the rows from 40 to 60.

# In[28]:


sorted_data = data.sort_values(by = ['likes'], ascending = False)
third_twenty_popular_videos = sorted_data.iloc[40:60]


# In order to be able to compare the values between the first 20 popular videos and third ones, I am going to plot them using scatter plots. 

# In[29]:


x = most_popular_videos['likes']
y = most_popular_videos['views']
percentage = most_popular_videos['VCP']
f, ax = plt.subplots()
s1 = ax.scatter(x,y,edgecolor='black', c=percentage, cmap='summer'
            ,linewidth=1, alpha=0.75)
cbar=f.colorbar(s1)
cbar.set_label('commet counts/views ratio')
xlims = ax.get_xlim()
ylims = ax.get_ylim()
ax.plot(xlims, ylims, ls = '--')
plt.show()



# In[30]:


x2 = third_twenty_popular_videos['likes']
y2 = third_twenty_popular_videos['views']
percentage2 = third_twenty_popular_videos['VCP']
f, ax = plt.subplots()
s2 = ax.scatter(x2,y2,edgecolor='black', c=percentage2, cmap='summer'
            ,linewidth=1, alpha=0.75)

cbar=f.colorbar(s2)
cbar.set_label('commet counts/views ratio')
#ax.xlabel('number of likes')
#ax.ylabel('number of views')
xlims = ax.get_xlim()
ylims = ax.get_ylim()
ax.plot(xlims,ylims,ls='--')
plt.show()


# As it is expected, in the first scatter plot which relates to the first twenty most populer videos on youtube, there are more of yellowish and lightened circles. This is because apparently most popular videos attract more attention and motivates the viewers to leave a comment. Still in the same scatter plot, yellowish circles are concentrated more close to the diagonal line. Note that the diagonal line indicates the imaginary videos with the same number of likes as the number of views. 
# Also, at the first glace it seems not possible to have the circles below the diagonal line (by the interpretation that the number of likes is more than the number of views for a video!!). However, note that the scales of the horizontal line (1e6) and the vertical line(1e8) refer to different scientific notations. In the second scatter plot, which is for the third twenty popular videos, the circles seems to be darker which means viewers were less eager to leave comments.

# ## Frequency of tagging words used in videos.

# Now, let's imagine the popular videos are those with higher numbers of comments. In our data frame, there is a column called tags, which indicates the words that are used to tag a video. These tags have an important role in attracting the viewers. So, it would be nice to see which tagging words cause to attract more viewers. There are different ways to do that. I am going to start with a way, which is not really the favorit way to do it in pandas, and then I will present another way with is more appropriate.

# ### The first approach:

# First, let's take a look at the tags column of the data frame:

# In[33]:


data['tags']


# As you can see, there are different words in different languages that are used to tag videos, and they are separated using ```"|"```. Also, there are some videos that did not use tags and in their corresponding cell, there is a ```[none]```. So the fist things that I should do is to remove the none values and also separate the words in each row of the ```tags``` column. I am going to remove all the cells with none values from the pandas Series, and then I am going to convert it as a list, and from there, I will use python capabilities to separate and count the words. Let's refer to the pandas Series ```data['tags']``` as vatriable **tags**.

# In[34]:


tags = data['tags']


# Then from tags I need to remove all ```[none]```values. There is also a classical non-value in data frames which is **NAN**. First, I use the method **dropna( )** in order to get read of all possible NAN values. As a note, in pandas NAN value is of type float.

# In[35]:


tags.dropna(inplace = True)


# Now To remove ```[none]```values, I can convert ```tags```to a list using the method tolist, and then, I use a list comprehension to just keep the values which are not ```[none]```.

# In[36]:


tag_list = tags.tolist()


# In[37]:


tag_list = [value for value in tag_list if value !='[none]']


# Also, since there is a possiblity that one word is repeated in both lowercase and uppercase, I just change all the words to be lowercase in order to count all different forms of a word in the ```tags```column.

# In[38]:


tag_ls = [x.lower() for x in tag_list]
tag_ls


# It seems that now all the values of the list are strings of words separated by a delimiter ```"|"```. Now, it order to separate the words for each string, I am using a for loop and apply the split method in order to separete the tagging words.
# 
# At the same time, I want to count the frequency of words in each string of the list. To do that, I am using the **Counter** object of python. Counter object, is an object that creates an ordered dictionary whose keys are whatever we want to count(here words), and its values are the frequency of the keys. In order to use the Counter object we need to import it from ```collections```.

# In[39]:


from collections import Counter


# In the following, I use the **update( )** method of the Counter to update its values after reading and splitting each of the strings in ```tag_list```.

# In[41]:


c = Counter()
for row in tag_ls:
    r = row.split('"|"')
    c.update(r)


# The interesting thing about Counter object is the possibility to use a method named **most_common**, which returns an ordered list of the most common keys of the ordered dictionary according to the frequencies. To get the fifteen most common words in our example, it is sufficient to pass the number 15 as an argument to the method.

# In[42]:


print(c.most_common(15)) 


# Now I can visualise the results using a horizontal bar. 

# In[44]:


names = []
frequencies = []
for item in c.most_common(15):
    names.append(item[0])
    frequencies.append(item[1])
    
plt.barh(names, frequencies, color = 'blue') 
plt.show()


# Of course, to represent it much nicer I can reverse the lists names and frequencies, use a nice style **fivethirtyeight**, and add some titles and labels.

# In[45]:


names.reverse()
frequencies.reverse()
plt.style.use('fivethirtyeight')
plt.barh(names,frequencies,color = 'blue')
plt.xlabel('Frequency of the tagging words')
plt.ylabel('Names of the 15 most common tagging words')
plt.title('Analysing the popularity of tagging words')
plt.show()


# ### The second approach:

# To show how powerful is pandas, in below, I have used more of fonctionalities provided by pandas to do the same analyse on the popularity of tagging words.

# In pandas, each column of a data frame is a pandas Series. And there are specific methods that can be used to work with pandas Series, which are called **string methods**. In my example, since I want to work with ```tags```column of the data frame, the string methods are a great help. 
# 
# Also, one of the very practical features of pandas, are filters. Filters make it possible to choose specific values in a dataframe that meet some pre-defined conditions. So, I am going to create a filter which allows me to select values in the tags column of the dataframe that contain ```"|"```, and then I will use the string method split, in order to separate the tagging words in all cells of the column at the same time.

# Pandas Series have a method called contains or more precisely **str.contains** that verify if values in a pandas Series contain specific value or not. If yes it returs a value of ```True``` and if not it returs a value of ```False```. I am using this method to create a filter to mask cells that do not contain ```"|"```. In this way, I can get rid of all ```[none]```or ```NAN```values in the column.

# In[46]:


filt = data['tags'].str.contains('"|"')


# Now that I create the filter I can use it in the pandas serie to choose the values that I want i.e., values with at least one ```"|"``` inside it.

# In[47]:


new_tags = data.loc[filt,'tags']


# Now to split the strings in each row of the ```tags``` column I use the string method split, and as an argument I will pass **Reqular Expressions** to it. There is a useful documentation about the reqular expressions in  (https://docs.python.org/3/library/re.html). As a regular expression here I use the character set ```["|"]``` followed by a ```+```. It means that search in the string, and as it reaches to at least one of the possible combinations of ```"```, and ```|```, split the string from there. Also, since words may present both in lowercase and uppercase letters, I simply convert all of the words to lower case by the string method **str.lower**.

# In[48]:


l_tags = new_tags.str.lower()


# In[49]:


ls_tags = l_tags.str.split((r'["|"]+'))


# If I see the ```ls_tags```, I can see that all the rows of the ```tags```column are nicely sepatated to words, and the words are ready to be counted.

# In[50]:


ls_tags


# To count the words I again use the ```Counter```, and update it by list of words in each row of ```ls_tags```.

# In[51]:


c = Counter()
for row in ls_tags:
    c.update(row)
del c['']    
print(c.most_common(15))


# In[53]:


trends = c.most_common(15)
names=[item[0] for item in trends ]
frequency = [item[1] for item in trends]
names.reverse()
frequency.reverse()
plt.style.use('fivethirtyeight')
plt.barh(names,frequency, color ='blue')
plt.show()


# At is it given, the result of the second approach is the same as that of the first approach, with mush less coding.

# ## The number of videos published by each channel

# One functionality of pandas, is to group a dataframe based on a specific parameter. For instance, in the dataframe of youtube videos, it might be helpful to group the information based on youtube channels. In this case, I can count, for example, the number of videos published by a channel, or verify which channel is more popular based on the number of comments it has received. To group the information, there is a method called **groupby( )**. Let's again overview the dataframe **data**.

# In[54]:


data


# In the following, the method groupby() is applied to group the dataframe data using the information in the column ```channel_title```.

# In[56]:


channel_group = data.groupby(['channel_title'])


# Using the attribute **groups**, I can retrieve a dictionary whose keys are the name of groups and whose values are the labels to those groups.

# So to get the list of all group names, it is possible to refer to the keys of the dictionary.

# In[57]:


channel_group.groups.keys()


# I am going to use the grouped dataframe and count the number of videos published by each youtube channel. To do that it is sufficient to count, for each group, the values in the ```title``` column of the data frame.

# In[59]:


channel_group['title'].count()


# To be more clear, let's order the counts in descending order.

# In[60]:


channel_group['title'].count().sort_values(ascending = False)


# Note that the output of  ```channel_group['title'].count()``` is a pandas series, indexed by channel names. I can get the twenty more active youtube channels as below:

# In[61]:


channel_group['title'].count().nlargest(20)


# Another way to get the number of videos published by each youtube channel, is to use the method value_counts( ) over the column **channel_title**  of the main dataframe **data**.

# In[62]:


data['channel_title'].value_counts()


# As another practice, it might be interesting to see, what percentage of videos published by the most active youtube channels have received comments more than, let's say, 1000.

# To do that, I should get for each youtube channel, the number of all published videos (that I have already got it), and I also compute, for each channel, how many videos have got more than ```1000```comments. In below, I have used the method apply over the grouped dataframe **channel_group** to get the videos with more than 1000 comments. Note that in this case, the function that is passed as an argument inside the apply method has a subframe as its input. Each subframe represents a group of information in the grouped dataframe. Therefore, in the following, ```x``` of the lambda function is, in fact, a subframe in the grouped dataframe **chennel_group**. I have used a filter **x > 1000** for each subframe ```x``` to get the favorit values. 

# In[64]:


nbr_videos_popular = channel_group['comment_count'].apply(lambda x : (x[x > 1000]).count()).sort_values(ascending = False)


# The total number of videos published by each channel has already been computed in two ways. However, as the third way, I am going to recompute it again as below.

# In[65]:


total_videos_for_each_channel = channel_group['comment_count'].apply(lambda x : x.count())


# Now, one way to continue is to concatenate the two pandas Series and form a new data frame, and add a new column to it in which the percentages have been stored. It can be done as below.

# In[66]:


data_concat = pd.concat([nbr_videos_popular , total_videos_for_each_channel], keys =['nbv_comment > 1000','Tnbv'], axis = 'columns')
data_concat


# The percentage column of the new dataframe is created as below:

# In[67]:


data_concat['percentage'] = (data_concat['nbv_comment > 1000']/data_concat['Tnbv'])* 100
data_concat.loc['Troom Troom FR']


# Let's take a loot at the **data_concat** dataframe.

# In[68]:


data_concat


# From the calculated data frame one can get many useful information. For instance, I can verify for channel **Troom Troom FR**, which is the most active one, that only a small percentage of videos have got more than 1000 comments, just 27 percent of its videos!

# In[69]:


data_concat.loc['Troom Troom FR']['percentage']


# In[ ]:




