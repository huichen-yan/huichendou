
def setup_tensorflow():
    """TensorFlow配置函数"""
    import os
    import tensorflow as tf

    # 关闭oneDNN优化
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

    # 设置日志级别 (0=所有, 1=INFO过滤, 2=WARNING过滤, 3=ERROR过滤)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # 设置Python日志级别
    tf.get_logger().setLevel('ERROR')

    # 可选：关闭eager execution的警告
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


