import os
import scipy.misc
import numpy as np

from model import DCGAN
from utils import pp, visualize, to_json, show_all_variables

import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_integer("epoch", 25, "Epoch to train [25]")
flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")
flags.DEFINE_integer("train_size", np.inf, "The size of train images [np.inf]")
flags.DEFINE_integer("batch_size", 64, "The size of batch images [64]")
flags.DEFINE_integer("input_height", 108, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_integer("input_width", None, "The size of image to use (will be center cropped). If None, same value as input_height [None]")
flags.DEFINE_integer("output_height", 64, "The size of the output images to produce [64]")
flags.DEFINE_integer("output_width", None, "The size of the output images to produce. If None, same value as output_height [None]")
flags.DEFINE_integer("c_dim", 3, "Dimension of image color. [3]")
flags.DEFINE_integer("z_dim", 100, "Dimension of laten var color. [100]")
flags.DEFINE_string("dataset", "celebA", "The name of dataset [celebA, mnist, lsun]")
flags.DEFINE_string("input_fname_pattern", "*.jpg", "Glob pattern of filename of input images [*]")
flags.DEFINE_string("checkpoint_dir_read", "checkpoint", "Directory name to read the checkpoints [checkpoint]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("sample_dir", "output", "Directory name to save the image samples [output]")
flags.DEFINE_boolean("is_train", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("is_crop", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("visualize", False, "True for visualizing, False for nothing [False]")
flags.DEFINE_boolean("on_cloud", 0, "If the program will be executed on the cloud or not [0]")
FLAGS = flags.FLAGS

def main(_):
  

  pp.pprint(flags.FLAGS.__flags)

  if FLAGS.input_width is None:
    FLAGS.input_width = FLAGS.input_height
  if FLAGS.output_width is None:
    FLAGS.output_width = FLAGS.output_height

  if FLAGS.on_cloud is None:
    FLAGS.on_cloud = 0;

  if FLAGS.on_cloud==0:
    checkpoint_dir_t = os.path.join(FLAGS.checkpoint_dir)
    if not os.path.exists(checkpoint_dir_t):
      os.makedirs(checkpoint_dir_t)
    sample_dir_t = os.path.join("./output/",FLAGS.sample_dir)
    if not os.path.exists(sample_dir_t):
      os.makedirs(sample_dir_t)
      os.makedirs(sample_dir_t+'/tests')
      os.makedirs(sample_dir_t+'/logs')
  elif FLAGS.on_cloud==1:
    checkpoint_dir_t = os.path.join("/output/",FLAGS.checkpoint_dir)
    if not os.path.exists(checkpoint_dir_t):
      os.makedirs(checkpoint_dir_t)
    sample_dir_t = os.path.join("/output/",FLAGS.sample_dir)
    if not os.path.exists(sample_dir_t):
      os.makedirs(sample_dir_t)
      os.makedirs(sample_dir_t+'/tests')
      os.makedirs(sample_dir_t+'/logs')


  #gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
  run_config = tf.ConfigProto()
  run_config.gpu_options.allow_growth=True

  with tf.Session(config=run_config) as sess:

    dcgan = DCGAN(
        sess,
        input_width=FLAGS.input_width,
        input_height=FLAGS.input_height,
        output_width=FLAGS.output_width,
        output_height=FLAGS.output_height,
        batch_size=FLAGS.batch_size,
        c_dim=FLAGS.c_dim,
        z_dim=FLAGS.z_dim,
        dataset_name=FLAGS.dataset,
        input_fname_pattern=FLAGS.input_fname_pattern,
        is_crop=FLAGS.is_crop,
        checkpoint_dir_read=FLAGS.checkpoint_dir_read,
        checkpoint_dir=FLAGS.checkpoint_dir,
        sample_dir=FLAGS.sample_dir,
        on_cloud=FLAGS.on_cloud)

    show_all_variables()
    if FLAGS.is_train:
      dcgan.train(FLAGS)
    else:
      if not dcgan.load(FLAGS.checkpoint_dir):
        raise Exception("[!] Train a model first, then run test mode")
      

    # to_json("./web/js/layers.js", [dcgan.h0_w, dcgan.h0_b, dcgan.g_bn0],
    #                 [dcgan.h1_w, dcgan.h1_b, dcgan.g_bn1],
    #                 [dcgan.h2_w, dcgan.h2_b, dcgan.g_bn2],
    #                 [dcgan.h3_w, dcgan.h3_b, dcgan.g_bn3],
    #                 [dcgan.h4_w, dcgan.h4_b, None])

    # Below is codes for visualization
    OPTION = 1
    visualize(sess, dcgan, FLAGS, OPTION,FLAGS.on_cloud,FLAGS.sample_dir)

if __name__ == '__main__':
  tf.app.run()
