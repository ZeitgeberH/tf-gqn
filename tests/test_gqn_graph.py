"""
Quick test script to check graph definition of full GQN model.
"""

import tensorflow as tf
import numpy as np

from gqn.gqn_params import PARAMS
from gqn.gqn_graph import gqn

# constants
_BATCH_SIZE = 1
_CONTEXT_SIZE = PARAMS.CONTEXT_SIZE
_DIM_POSE = PARAMS.POSE_CHANNELS
_DIM_H_IMG = PARAMS.IMG_HEIGHT
_DIM_W_IMG = PARAMS.IMG_WIDTH
_DIM_C_IMG = PARAMS.IMG_CHANNELS
_SEQ_LENGTH = PARAMS.SEQ_LENGTH

# input placeholders
query_pose = tf.placeholder(
    shape=[_BATCH_SIZE, _DIM_POSE], dtype=tf.float32)
target_frame = tf.placeholder(
    shape=[_BATCH_SIZE, _DIM_H_IMG, _DIM_W_IMG, _DIM_C_IMG],
    dtype=tf.float32)
context_poses = tf.placeholder(
    shape=[_BATCH_SIZE, _CONTEXT_SIZE, _DIM_POSE],
    dtype=tf.float32)
context_frames = tf.placeholder(
    shape=[_BATCH_SIZE, _CONTEXT_SIZE, _DIM_H_IMG, _DIM_W_IMG, _DIM_C_IMG],
    dtype=tf.float32)

# graph definition
net, ep_gqn = gqn(
    query_pose=query_pose,
    target_frame=target_frame,
    context_poses=context_poses,
    context_frames=context_frames,
    model_params=PARAMS,
    is_training=True
)

# feed random input through the graph
with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  mu = sess.run(
      net,
      feed_dict={
          query_pose : np.random.rand(_BATCH_SIZE, _DIM_POSE),
          target_frame : np.random.rand(_BATCH_SIZE, _DIM_H_IMG, _DIM_W_IMG, _DIM_C_IMG),
          context_poses : np.random.rand(_BATCH_SIZE, _CONTEXT_SIZE, _DIM_POSE),
          context_frames : np.random.rand(_BATCH_SIZE, _CONTEXT_SIZE, _DIM_H_IMG, _DIM_W_IMG, _DIM_C_IMG),
      })
  print(mu)
  print(mu.shape)
  for ep, t in ep_gqn.items():
    print(ep, t)
