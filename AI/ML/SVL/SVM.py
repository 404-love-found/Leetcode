import pandas as pd                                   # tables (DataFrame)
import matplotlib.pyplot as plt                       # plotting
from sklearn.model_selection import train_test_split  # split into train / test
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_auc_score

import warnings
warnings.filterwarnings('ignore')                     # hide warning messages

# ===== 1. Load data =====
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%203/data/creditcard.csv"
raw_data = pd.read_csv(url)                           # DataFrame, shape (284807, 31)
print("data information:")
raw_data.info()                                       

# ===== 2. Class balance pie chart =====
counts = raw_data['Class'].value_counts()             # one Series holds both labels and sizes
labels = counts.index                                 # [0, 1]  (same order as sizes, guaranteed)
sizes = counts.values                                 # [284315, 492]
fig, ax = plt.subplots()                              # one figure + one Axes
ax.pie(sizes, labels=labels, autopct='%1.3f%%')       # pie chart, percentage with 3 decimals
ax.set_title('Target Variable Value Counts')
plt.show()

# ===== 3. Correlation of each feature with Class =====
Correlation_values = raw_data.corr(numeric_only=True)['Class'].drop('Class')   
ax = Correlation_values.plot(kind='barh', figsize=(10, 6))   # horizontal bars, returns an Axes
ax.set_title('Correlation with Class')
plt.show()                                            # ★ changed: needed in a .py script

# ===== 4. Preprocessing =====
# columns 1..29 = V1..V28 + Amount (column 0 is Time, column 30 is Class)
raw_data.iloc[:, 1:30] = StandardScaler().fit_transform(raw_data.iloc[:, 1:30])
data_matrix = raw_data.values                         # DataFrame -> numpy ndarray, shape (284807, 31)
X = data_matrix[:, 1:30]                              # features, shape (284807, 29), Time excluded
y = data_matrix[:, 30]                                # labels, shape (284807,)
X = normalize(X, norm="l1")                           # each ROW's absolute values now sum to 1

# ===== 5. Train / test split =====
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ===== 6. Decision tree =====
w_train = compute_sample_weight('balanced', y_train)  # fraud rows get a much bigger weight
dt = DecisionTreeClassifier(max_depth=4, random_state=35)
dt.fit(X_train, y_train, sample_weight=w_train)

# ===== 7. Linear SVM =====
SVM = LinearSVC(class_weight='balanced', random_state=42, loss='hinge', fit_intercept=False)
SVM.fit(X_train, y_train)                             # ★ changed: was SVM.fit(X, y), which includes the test set

# ===== 8. Evaluate =====
y_pred_dt = dt.predict_proba(X_test)[:, 1]            # probability of fraud for each test row
roc_auc_dt = roc_auc_score(y_test, y_pred_dt)
print('Decision Tree ROC-AUC score : {0:.3f}'.format(roc_auc_dt))

y_pred_svm = SVM.decision_function(X_test)            # signed distance to the boundary (bigger = more fraud-like)
roc_auc_svm = roc_auc_score(y_test, y_pred_svm)
print("SVM ROC-AUC score: {0:.3f}".format(roc_auc_svm))

