# algorithm	             # function	                                     # type of return
.values                 去掉列名和行号，只留数字                             ndarray，shape (n, 16)
.to_numpy()             同样的功能，pandas 现在更推荐这种写法                 ndarray



# split the data
train_test_split(X, y, test_size=0.3, random_state=42)

# check the missing values
.isnull().sum() 

# check the correlation
corr = data.corr(numeric_only=True)['Y'].drop('Y') # Y is the predict value
corr.sort_values(ascending=False) #Correlation Sorts by value #Ascending=False for large to small
corr.plot(kind='barh', figsize=(10, 6)) 
#kind='bar' vertical bars, 'barh' horizontal bars, 'line' line chart (default), 'hist' histogram 
#figsize=(width, height)

# Visualize

plt.show()		            #Actually displays the chart you drew
plt.tight_layout()		    #Adjusts margins automatically
ax.set_title('...')	 	    #Adds a title to that plotting area

# data processing
data.index		          #Shows the index (here, the column names)
data.values	              #Just the values, as an ndarray
data.abs()	              #Absolute value of each entry, returns a new Series

# Model build
DecisionTreeRegressor(criterion='squared_error', max_depth=d, random_state=42) 
#depth is the number of cuts
