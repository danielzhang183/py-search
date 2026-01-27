# 数据清洗高级技巧

> 从基础到高级的数据清洗实战指南

## 📋 目录

1. [数据清洗概述](#数据清洗概述)
2. [文本清洗高级技巧](#文本清洗高级技巧)
3. [数据质量检测](#数据质量检测)
4. [异常值处理](#异常值处理)
5. [数据标准化与规范化](#数据标准化与规范化)
6. [去重策略](#去重策略)
7. [数据验证与修复](#数据验证与修复)
8. [性能优化技巧](#性能优化技巧)
9. [实战案例](#实战案例)
10. [工具和库推荐](#工具和库推荐)

---

## 数据清洗概述

### 什么是数据清洗？

数据清洗（Data Cleaning）是指检测、修正或删除数据集中不准确、不完整、格式错误或重复的数据的过程。

### 数据清洗的重要性

- **提高数据质量**：确保数据准确性和一致性
- **提升分析效果**：干净的数据产生更可靠的分析结果
- **减少错误**：避免因脏数据导致的业务决策错误
- **节省时间**：自动化清洗流程，提高效率

### 常见数据问题

1. **缺失值**：空值、NULL、NaN
2. **格式不一致**：日期格式、电话号码格式
3. **重复数据**：完全重复、部分重复
4. **异常值**：超出合理范围的值
5. **拼写错误**：人名、地名、产品名
6. **编码问题**：字符编码、特殊字符
7. **不一致性**：同一实体的不同表示

---

## 文本清洗高级技巧

### 1. 多语言文本处理

```python
import unicodedata
import re

def normalize_unicode(text):
    """Unicode标准化"""
    if not text:
        return ""
    
    # NFC标准化（推荐用于显示）
    text = unicodedata.normalize('NFC', text)
    
    # 移除零宽字符
    text = re.sub(r'[\u200b-\u200d\ufeff]', '', text)
    
    return text

def remove_control_characters(text):
    """移除控制字符"""
    return ''.join(char for char in text 
                   if unicodedata.category(char)[0] != 'C')

# 使用示例
text = "Hello\u200bWorld"  # 包含零宽空格
cleaned = normalize_unicode(text)
```

### 2. 智能空白处理

```python
import re

def smart_whitespace_clean(text):
    """智能空白处理"""
    if not text:
        return ""
    
    # 保留中文之间的空格（可选）
    # 移除其他多余空白
    text = re.sub(r'[ \t]+', ' ', text)  # 多个空格/制表符 -> 单个空格
    text = re.sub(r'\n{3,}', '\n\n', text)  # 多个换行 -> 两个换行
    text = re.sub(r'[ \t]+\n', '\n', text)  # 行尾空白
    text = re.sub(r'\n[ \t]+', '\n', text)  # 行首空白
    
    return text.strip()

# 处理混合空白字符
text = "Hello    World\n\n\nTest\t\tValue"
cleaned = smart_whitespace_clean(text)
```

### 3. 上下文感知的文本清理

```python
def context_aware_clean(text, preserve_urls=True, preserve_emails=True):
    """上下文感知的文本清理"""
    if not text:
        return ""
    
    # 保存URL和邮箱（如果需要）
    placeholders = {}
    
    if preserve_urls:
        urls = re.findall(r'https?://[^\s]+', text)
        for i, url in enumerate(urls):
            placeholder = f"__URL_{i}__"
            placeholders[placeholder] = url
            text = text.replace(url, placeholder)
    
    if preserve_emails:
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        for i, email in enumerate(emails):
            placeholder = f"__EMAIL_{i}__"
            placeholders[placeholder] = email
            text = text.replace(email, placeholder)
    
    # 执行清理
    text = re.sub(r'[^\w\s.,!?;:()\-\'"]', '', text)  # 移除特殊字符
    
    # 恢复占位符
    for placeholder, original in placeholders.items():
        text = text.replace(placeholder, original)
    
    return text
```

### 4. 模糊匹配去重

```python
from difflib import SequenceMatcher
from collections import defaultdict

def fuzzy_deduplicate(texts, threshold=0.85):
    """模糊匹配去重"""
    unique_texts = []
    seen_groups = defaultdict(list)
    
    for text in texts:
        text_clean = text.lower().strip()
        is_duplicate = False
        
        for group_key, group_texts in seen_groups.items():
            similarity = SequenceMatcher(None, text_clean, group_key).ratio()
            if similarity >= threshold:
                seen_groups[group_key].append(text)
                is_duplicate = True
                break
        
        if not is_duplicate:
            seen_groups[text_clean] = [text]
            unique_texts.append(text)
    
    return unique_texts, seen_groups

# 使用示例
texts = [
    "Apple Inc.",
    "Apple Inc",
    "apple inc.",
    "Microsoft Corp",
    "Microsoft Corporation"
]
unique, groups = fuzzy_deduplicate(texts, threshold=0.9)
```

### 5. 正则表达式优化

```python
import re

# 编译正则表达式（性能优化）
PHONE_PATTERN = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
URL_PATTERN = re.compile(r'https?://[^\s]+')

def extract_structured_data(text):
    """提取结构化数据"""
    return {
        'phones': PHONE_PATTERN.findall(text),
        'emails': EMAIL_PATTERN.findall(text),
        'urls': URL_PATTERN.findall(text),
    }
```

### 6. 文本规范化（大小写、缩写）

```python
import re

ABBREVIATIONS = {
    'inc.': 'Inc.',
    'corp.': 'Corp.',
    'ltd.': 'Ltd.',
    'co.': 'Co.',
}

def normalize_text(text, title_case=True):
    """文本规范化"""
    if not text:
        return ""
    
    # 处理缩写
    for abbrev, replacement in ABBREVIATIONS.items():
        text = re.sub(rf'\b{re.escape(abbrev)}\b', replacement, text, flags=re.IGNORECASE)
    
    # 标题大小写（智能）
    if title_case:
        # 保持缩写大写
        words = text.split()
        normalized = []
        for word in words:
            if word.lower() in [abbrev.lower() for abbrev in ABBREVIATIONS.keys()]:
                normalized.append(word)
            else:
                normalized.append(word.capitalize())
        text = ' '.join(normalized)
    
    return text
```

---

## 数据质量检测

### 1. 完整性检测

```python
import pandas as pd
import numpy as np

def check_completeness(df):
    """检查数据完整性"""
    total_rows = len(df)
    completeness_report = {}
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_percentage = (null_count / total_rows) * 100
        
        completeness_report[col] = {
            'total': total_rows,
            'null_count': null_count,
            'null_percentage': null_percentage,
            'completeness': 100 - null_percentage
        }
    
    return completeness_report

def detect_missing_patterns(df):
    """检测缺失值模式"""
    missing_matrix = df.isnull()
    
    # 完全缺失的列
    completely_missing = missing_matrix.all()
    
    # 缺失值模式
    missing_patterns = {}
    for col in df.columns:
        if missing_matrix[col].any():
            missing_patterns[col] = {
                'pattern': 'random' if missing_matrix[col].sum() < len(df) * 0.5 else 'systematic',
                'missing_indices': missing_matrix[col][missing_matrix[col]].index.tolist()
            }
    
    return {
        'completely_missing': completely_missing[completely_missing].index.tolist(),
        'patterns': missing_patterns
    }
```

### 2. 一致性检测

```python
def check_consistency(df, rules=None):
    """检查数据一致性"""
    inconsistencies = []
    
    # 默认规则
    if rules is None:
        rules = {
            'date_format': r'\d{4}-\d{2}-\d{2}',
            'email_format': r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$',
        }
    
    for col in df.columns:
        # 检查格式一致性
        if col.endswith('_date') or 'date' in col.lower():
            invalid_dates = df[~df[col].astype(str).str.match(rules['date_format'], na=False)]
            if len(invalid_dates) > 0:
                inconsistencies.append({
                    'column': col,
                    'type': 'date_format',
                    'count': len(invalid_dates),
                    'examples': invalid_dates[col].head(5).tolist()
                })
        
        if col.endswith('_email') or 'email' in col.lower():
            invalid_emails = df[~df[col].astype(str).str.match(rules['email_format'], na=False)]
            if len(invalid_emails) > 0:
                inconsistencies.append({
                    'column': col,
                    'type': 'email_format',
                    'count': len(invalid_emails),
                    'examples': invalid_emails[col].head(5).tolist()
                })
    
    return inconsistencies
```

### 3. 准确性检测

```python
def validate_data_ranges(df, schema):
    """验证数据范围"""
    """
    schema = {
        'age': {'min': 0, 'max': 150},
        'price': {'min': 0, 'max': 1000000},
        'rating': {'min': 1, 'max': 5},
    }
    """
    violations = []
    
    for col, rules in schema.items():
        if col not in df.columns:
            continue
        
        if 'min' in rules:
            below_min = df[df[col] < rules['min']]
            if len(below_min) > 0:
                violations.append({
                    'column': col,
                    'rule': f'min={rules["min"]}',
                    'count': len(below_min),
                    'examples': below_min[col].head(5).tolist()
                })
        
        if 'max' in rules:
            above_max = df[df[col] > rules['max']]
            if len(above_max) > 0:
                violations.append({
                    'column': col,
                    'rule': f'max={rules["max"]}',
                    'count': len(above_max),
                    'examples': above_max[col].head(5).tolist()
                })
    
    return violations
```

---

## 异常值处理

### 1. 统计方法检测异常值

```python
import numpy as np
import pandas as pd

def detect_outliers_iqr(df, column):
    """使用IQR方法检测异常值"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    return {
        'outliers': outliers,
        'bounds': {'lower': lower_bound, 'upper': upper_bound},
        'count': len(outliers),
        'percentage': (len(outliers) / len(df)) * 100
    }

def detect_outliers_zscore(df, column, threshold=3):
    """使用Z-score方法检测异常值"""
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    outliers = df[z_scores > threshold]
    
    return {
        'outliers': outliers,
        'z_scores': z_scores,
        'count': len(outliers),
        'percentage': (len(outliers) / len(df)) * 100
    }

def detect_outliers_isolation_forest(df, columns, contamination=0.1):
    """使用Isolation Forest检测异常值"""
    from sklearn.ensemble import IsolationForest
    
    # 只处理数值列
    numeric_cols = df[columns].select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        return None
    
    X = df[numeric_cols].fillna(df[numeric_cols].median())
    
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    predictions = iso_forest.fit_predict(X)
    
    outliers = df[predictions == -1]
    
    return {
        'outliers': outliers,
        'count': len(outliers),
        'percentage': (len(outliers) / len(df)) * 100,
        'scores': iso_forest.score_samples(X)
    }
```

### 2. 异常值处理策略

```python
def handle_outliers(df, column, method='clip', **kwargs):
    """处理异常值"""
    if method == 'remove':
        # 删除异常值
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return df[(df[column] >= lower) & (df[column] <= upper)]
    
    elif method == 'clip':
        # 截断到边界值
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        df_cleaned = df.copy()
        df_cleaned[column] = df_cleaned[column].clip(lower=lower, upper=upper)
        return df_cleaned
    
    elif method == 'replace':
        # 替换为统计值
        replace_value = kwargs.get('replace_value', df[column].median())
        df_cleaned = df.copy()
        
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        
        mask = (df[column] < lower) | (df[column] > upper)
        df_cleaned.loc[mask, column] = replace_value
        return df_cleaned
    
    elif method == 'transform':
        # 对数变换（适用于右偏分布）
        df_cleaned = df.copy()
        df_cleaned[column] = np.log1p(df_cleaned[column])
        return df_cleaned
    
    return df
```

---

## 数据标准化与规范化

### 1. 日期时间标准化

```python
from datetime import datetime
import pandas as pd
import re

def normalize_date(date_str, formats=None):
    """标准化日期格式"""
    if pd.isna(date_str) or date_str == '':
        return None
    
    if formats is None:
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%m-%d-%Y',
            '%m/%d/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
            '%d-%m-%Y %H:%M:%S',
        ]
    
    date_str = str(date_str).strip()
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    # 尝试自动解析
    try:
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except:
        return None

def normalize_datetime_series(series):
    """标准化日期时间序列"""
    return series.apply(normalize_date)
```

### 2. 电话号码标准化

```python
import re

def normalize_phone(phone_str, country_code='+86'):
    """标准化电话号码"""
    if not phone_str or pd.isna(phone_str):
        return None
    
    # 移除所有非数字字符（除了+）
    phone = re.sub(r'[^\d+]', '', str(phone_str))
    
    # 移除前导0
    phone = phone.lstrip('0')
    
    # 处理国家代码
    if phone.startswith('+'):
        return phone
    elif phone.startswith('86') and len(phone) > 10:
        return '+' + phone
    elif len(phone) == 11 and phone.startswith('1'):
        return country_code + phone
    elif len(phone) == 10:
        return country_code + phone
    
    return phone

def normalize_phone_series(series):
    """标准化电话号码序列"""
    return series.apply(normalize_phone)
```

### 3. 地址标准化

```python
import re

ADDRESS_ABBREVIATIONS = {
    'street': 'St.',
    'avenue': 'Ave.',
    'road': 'Rd.',
    'boulevard': 'Blvd.',
    'drive': 'Dr.',
    'lane': 'Ln.',
}

def normalize_address(address_str):
    """标准化地址"""
    if not address_str or pd.isna(address_str):
        return None
    
    address = str(address_str).strip()
    
    # 统一缩写
    for full, abbrev in ADDRESS_ABBREVIATIONS.items():
        address = re.sub(rf'\b{full}\b', abbrev, address, flags=re.IGNORECASE)
    
    # 移除多余空格
    address = re.sub(r'\s+', ' ', address)
    
    # 标准化大小写
    address = address.title()
    
    return address
```

### 4. 数值标准化

```python
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def normalize_numeric(df, columns, method='standard'):
    """标准化数值列"""
    df_cleaned = df.copy()
    
    for col in columns:
        if col not in df.columns:
            continue
        
        if method == 'standard':
            # Z-score标准化
            scaler = StandardScaler()
            df_cleaned[col] = scaler.fit_transform(df_cleaned[[col]])
        
        elif method == 'minmax':
            # Min-Max标准化（0-1）
            scaler = MinMaxScaler()
            df_cleaned[col] = scaler.fit_transform(df_cleaned[[col]])
        
        elif method == 'robust':
            # 鲁棒标准化（使用中位数和IQR）
            scaler = RobustScaler()
            df_cleaned[col] = scaler.fit_transform(df_cleaned[[col]])
        
        elif method == 'log':
            # 对数变换
            df_cleaned[col] = np.log1p(df_cleaned[col])
    
    return df_cleaned
```

---

## 去重策略

### 1. 精确去重

```python
def exact_deduplicate(df, columns=None):
    """精确去重"""
    if columns is None:
        return df.drop_duplicates()
    else:
        return df.drop_duplicates(subset=columns)
```

### 2. 模糊去重

```python
from difflib import SequenceMatcher
from rapidfuzz import fuzz, process

def fuzzy_deduplicate_dataframe(df, key_column, threshold=85):
    """DataFrame模糊去重"""
    unique_values = []
    duplicate_groups = {}
    
    for idx, row in df.iterrows():
        value = str(row[key_column])
        
        # 使用rapidfuzz进行快速模糊匹配
        if unique_values:
            match = process.extractOne(value, unique_values, scorer=fuzz.ratio)
            if match and match[1] >= threshold:
                # 找到相似值，归入同一组
                matched_value = match[0]
                if matched_value not in duplicate_groups:
                    duplicate_groups[matched_value] = [matched_value]
                duplicate_groups[matched_value].append(value)
                continue
        
        unique_values.append(value)
    
    # 创建去重后的DataFrame
    df_cleaned = df[df[key_column].isin(unique_values)].copy()
    
    return df_cleaned, duplicate_groups
```

### 3. 基于相似度的去重

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity_based_deduplicate(texts, threshold=0.9):
    """基于相似度的去重"""
    if len(texts) == 0:
        return []
    
    # TF-IDF向量化
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    
    # 计算相似度矩阵
    similarity_matrix = cosine_similarity(vectors)
    
    # 找出相似文本
    seen = set()
    unique_indices = []
    
    for i in range(len(texts)):
        if i in seen:
            continue
        
        unique_indices.append(i)
        # 找出所有相似的文本
        similar_indices = [j for j in range(i+1, len(texts)) 
                          if similarity_matrix[i][j] >= threshold]
        seen.update(similar_indices)
    
    return [texts[i] for i in unique_indices]
```

### 4. 基于规则的去重

```python
def rule_based_deduplicate(df, rules):
    """基于规则的去重"""
    """
    rules = {
        'email': {'keep': 'first', 'case_sensitive': False},
        'phone': {'normalize': True, 'keep': 'last'},
    }
    """
    df_cleaned = df.copy()
    
    for column, rule in rules.items():
        if column not in df.columns:
            continue
        
        # 标准化
        if rule.get('normalize', False):
            if column == 'phone':
                df_cleaned[column] = normalize_phone_series(df_cleaned[column])
            elif column == 'email':
                df_cleaned[column] = df_cleaned[column].str.lower()
        
        # 去重
        keep = rule.get('keep', 'first')
        df_cleaned = df_cleaned.drop_duplicates(
            subset=[column],
            keep=keep
        )
    
    return df_cleaned
```

---

## 数据验证与修复

### 1. 数据验证框架

```python
from typing import Callable, List, Dict, Any

class DataValidator:
    """数据验证器"""
    
    def __init__(self):
        self.rules = {}
    
    def add_rule(self, column: str, validator: Callable, error_message: str = None):
        """添加验证规则"""
        if column not in self.rules:
            self.rules[column] = []
        
        self.rules[column].append({
            'validator': validator,
            'error_message': error_message or f"Validation failed for {column}"
        })
    
    def validate(self, df) -> Dict[str, List[Dict]]:
        """验证数据"""
        errors = {}
        
        for column, rules in self.rules.items():
            if column not in df.columns:
                continue
            
            column_errors = []
            for rule in rules:
                invalid_rows = df[~df[column].apply(rule['validator'])]
                if len(invalid_rows) > 0:
                    column_errors.append({
                        'rule': rule['error_message'],
                        'count': len(invalid_rows),
                        'indices': invalid_rows.index.tolist(),
                        'examples': invalid_rows[column].head(5).tolist()
                    })
            
            if column_errors:
                errors[column] = column_errors
        
        return errors

# 使用示例
validator = DataValidator()
validator.add_rule('email', lambda x: '@' in str(x), "Email must contain @")
validator.add_rule('age', lambda x: 0 <= x <= 150, "Age must be between 0 and 150")
validator.add_rule('phone', lambda x: len(str(x)) >= 10, "Phone must be at least 10 digits")

errors = validator.validate(df)
```

### 2. 自动修复

```python
class DataFixer:
    """数据自动修复器"""
    
    @staticmethod
    def fix_email(email_str):
        """修复邮箱"""
        if pd.isna(email_str):
            return None
        
        email = str(email_str).strip().lower()
        
        # 移除空格
        email = email.replace(' ', '')
        
        # 修复常见错误
        email = email.replace('@gmail.con', '@gmail.com')
        email = email.replace('@gmial.com', '@gmail.com')
        
        # 验证格式
        if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
            return email
        
        return None
    
    @staticmethod
    def fix_phone(phone_str):
        """修复电话号码"""
        return normalize_phone(phone_str)
    
    @staticmethod
    def fix_date(date_str):
        """修复日期"""
        return normalize_date(date_str)
    
    @staticmethod
    def fix_whitespace(text):
        """修复空白字符"""
        if pd.isna(text):
            return None
        return smart_whitespace_clean(str(text))

def auto_fix_dataframe(df, fix_rules):
    """自动修复DataFrame"""
    df_fixed = df.copy()
    
    for column, fix_method in fix_rules.items():
        if column not in df.columns:
            continue
        
        df_fixed[column] = df_fixed[column].apply(fix_method)
    
    return df_fixed

# 使用示例
fixer = DataFixer()
fix_rules = {
    'email': fixer.fix_email,
    'phone': fixer.fix_phone,
    'date': fixer.fix_date,
    'description': fixer.fix_whitespace,
}

df_fixed = auto_fix_dataframe(df, fix_rules)
```

---

## 性能优化技巧

### 1. 向量化操作

```python
# ❌ 慢：循环处理
def clean_texts_slow(texts):
    cleaned = []
    for text in texts:
        cleaned.append(text.strip().lower())
    return cleaned

# ✅ 快：向量化操作
def clean_texts_fast(texts):
    series = pd.Series(texts)
    return series.str.strip().str.lower().tolist()

# ✅ 更快：使用NumPy
import numpy as np
def clean_texts_faster(texts):
    arr = np.array(texts, dtype=object)
    return [str(x).strip().lower() if pd.notna(x) else '' for x in arr]
```

### 2. 批量处理

```python
def batch_process(df, func, batch_size=1000):
    """批量处理大数据"""
    results = []
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        batch_result = func(batch)
        results.append(batch_result)
    
    return pd.concat(results, ignore_index=True)
```

### 3. 并行处理

```python
from multiprocessing import Pool
import numpy as np

def parallel_clean(texts, num_workers=4):
    """并行文本清洗"""
    def clean_chunk(chunk):
        return [smart_whitespace_clean(str(text)) for text in chunk]
    
    # 分割数据
    chunks = np.array_split(texts, num_workers)
    
    # 并行处理
    with Pool(num_workers) as pool:
        results = pool.map(clean_chunk, chunks)
    
    # 合并结果
    return [item for sublist in results for item in sublist]
```

### 4. 缓存中间结果

```python
import pickle
import hashlib

def get_cache_key(data):
    """生成缓存键"""
    data_str = str(data)
    return hashlib.md5(data_str.encode()).hexdigest()

def cached_clean(text, cache_dir='.cache'):
    """带缓存的清洗"""
    cache_key = get_cache_key(text)
    cache_file = f"{cache_dir}/{cache_key}.pkl"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    # 执行清洗
    cleaned = smart_whitespace_clean(text)
    
    # 保存缓存
    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(cleaned, f)
    
    return cleaned
```

---

## 实战案例

### 案例1：清洗爬取的新闻数据

```python
import pandas as pd
from py_search.utils.text import clean_text, remove_html_tags

def clean_news_data(df):
    """清洗新闻数据"""
    df_cleaned = df.copy()
    
    # 1. 文本清洗
    if 'title' in df_cleaned.columns:
        df_cleaned['title'] = df_cleaned['title'].apply(
            lambda x: clean_text(remove_html_tags(str(x))) if pd.notna(x) else ''
        )
    
    if 'content' in df_cleaned.columns:
        df_cleaned['content'] = df_cleaned['content'].apply(
            lambda x: clean_text(remove_html_tags(str(x))) if pd.notna(x) else ''
        )
    
    # 2. 日期标准化
    if 'date' in df_cleaned.columns:
        df_cleaned['date'] = df_cleaned['date'].apply(normalize_date)
    
    # 3. URL规范化
    if 'link' in df_cleaned.columns:
        from py_search.utils.text import normalize_url
        df_cleaned['link'] = df_cleaned['link'].apply(
            lambda x: normalize_url(str(x)) if pd.notna(x) else None
        )
    
    # 4. 去重
    df_cleaned = df_cleaned.drop_duplicates(subset=['link'], keep='first')
    
    # 5. 移除空值行
    df_cleaned = df_cleaned.dropna(subset=['title', 'content'])
    
    return df_cleaned
```

### 案例2：清洗用户数据

```python
def clean_user_data(df):
    """清洗用户数据"""
    df_cleaned = df.copy()
    
    # 1. 邮箱标准化和验证
    if 'email' in df_cleaned.columns:
        fixer = DataFixer()
        df_cleaned['email'] = df_cleaned['email'].apply(fixer.fix_email)
        # 移除无效邮箱
        df_cleaned = df_cleaned[df_cleaned['email'].notna()]
    
    # 2. 电话号码标准化
    if 'phone' in df_cleaned.columns:
        df_cleaned['phone'] = df_cleaned['phone'].apply(normalize_phone)
    
    # 3. 姓名规范化
    if 'name' in df_cleaned.columns:
        df_cleaned['name'] = df_cleaned['name'].apply(
            lambda x: normalize_text(str(x), title_case=True) if pd.notna(x) else None
        )
    
    # 4. 地址标准化
    if 'address' in df_cleaned.columns:
        df_cleaned['address'] = df_cleaned['address'].apply(normalize_address)
    
    # 5. 年龄验证和异常值处理
    if 'age' in df_cleaned.columns:
        df_cleaned = handle_outliers(df_cleaned, 'age', method='clip')
        # 移除不合理年龄
        df_cleaned = df_cleaned[(df_cleaned['age'] >= 0) & (df_cleaned['age'] <= 150)]
    
    # 6. 去重（基于邮箱）
    df_cleaned = df_cleaned.drop_duplicates(subset=['email'], keep='last')
    
    return df_cleaned
```

### 案例3：清洗电商产品数据

```python
def clean_product_data(df):
    """清洗产品数据"""
    df_cleaned = df.copy()
    
    # 1. 价格清洗
    if 'price' in df_cleaned.columns:
        # 移除货币符号和空格
        df_cleaned['price'] = df_cleaned['price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df_cleaned['price'] = pd.to_numeric(df_cleaned['price'], errors='coerce')
        # 处理异常值
        df_cleaned = handle_outliers(df_cleaned, 'price', method='clip')
    
    # 2. 评分标准化（1-5分）
    if 'rating' in df_cleaned.columns:
        df_cleaned['rating'] = pd.to_numeric(df_cleaned['rating'], errors='coerce')
        df_cleaned['rating'] = df_cleaned['rating'].clip(lower=1, upper=5)
    
    # 3. 产品名称清洗
    if 'name' in df_cleaned.columns:
        df_cleaned['name'] = df_cleaned['name'].apply(
            lambda x: clean_text(str(x)) if pd.notna(x) else ''
        )
    
    # 4. 描述清洗
    if 'description' in df_cleaned.columns:
        df_cleaned['description'] = df_cleaned['description'].apply(
            lambda x: clean_text(remove_html_tags(str(x))) if pd.notna(x) else ''
        )
    
    # 5. SKU标准化（去除空格，转大写）
    if 'sku' in df_cleaned.columns:
        df_cleaned['sku'] = df_cleaned['sku'].astype(str).str.strip().str.upper()
    
    # 6. 去重（基于SKU）
    df_cleaned = df_cleaned.drop_duplicates(subset=['sku'], keep='first')
    
    return df_cleaned
```

---

## 工具和库推荐

### Python 库

1. **pandas** - 数据处理基础

   ```bash
   pip install pandas
   ```

2. **numpy** - 数值计算

   ```bash
   pip install numpy
   ```

3. **scikit-learn** - 机器学习工具（异常检测、标准化）

   ```bash
   pip install scikit-learn
   ```

4. **rapidfuzz** - 快速模糊匹配

   ```bash
   pip install rapidfuzz
   ```

5. **fuzzywuzzy** - 模糊字符串匹配

   ```bash
   pip install fuzzywuzzy python-Levenshtein
   ```

6. **pyjanitor** - 数据清洗工具

   ```bash
   pip install pyjanitor
   ```

7. **great-expectations** - 数据质量验证

   ```bash
   pip install great-expectations
   ```

8. **pydantic** - 数据验证

   ```bash
   pip install pydantic
   ```

### 实用工具

1. **OpenRefine** - 开源数据清洗工具
   - 网址：<https://openrefine.org/>

2. **Trifacta** - 商业数据清洗平台

3. **Pandas Profiling** - 自动生成数据报告

   ```bash
   pip install pandas-profiling
   ```

---

## 最佳实践总结

### 1. 清洗流程

```
原始数据
  ↓
数据质量检测
  ↓
缺失值处理
  ↓
格式标准化
  ↓
异常值处理
  ↓
去重
  ↓
验证
  ↓
清洗后数据
```

### 2. 关键原则

- **保留原始数据**：始终保留原始数据副本
- **记录清洗步骤**：记录所有清洗操作，便于追溯
- **验证清洗结果**：清洗后验证数据质量
- **自动化流程**：将清洗流程自动化，提高效率
- **性能优化**：对大数据使用向量化和并行处理

### 3. 常见陷阱

- ❌ 过度清洗：删除可能有用的数据
- ❌ 忽略上下文：不考虑数据业务含义
- ❌ 不验证结果：清洗后不检查数据质量
- ❌ 硬编码规则：不灵活的清洗逻辑
- ❌ 性能问题：对大数据使用低效方法

---

**祝您数据清洗顺利！** 🚀
