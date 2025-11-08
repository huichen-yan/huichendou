# tf_config.py
import os
# 必须在任何导入之前设置
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 设置为3更严格
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # 如果不需要GPU也禁用GPU相关日志

# 现在导入并配置tensorflow
import tensorflow as tf
tf.autograph.set_verbosity(0)
tf.get_logger().setLevel('ERROR')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)