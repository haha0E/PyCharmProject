import warnings

warnings.filterwarnings('ignore', '.*do not.*',)

warnings.warn('Show this message')
warnings.warn('Do not show this message')
# 写个例子，看看效果：
# Example of filtering warnings based on message content

# Filter warnings that contain the phrase 'ignore this'
warnings.filterwarnings('ignore', '.*ignore this.*')

# This warning will be shown
warnings.warn('This is a warning message')

# This warning will be ignored
warnings.warn('Please ignore this warning message')