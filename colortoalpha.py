#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Color To Alpha plug-in v1.0 by Seth Burgess, sjburges@gimp.org 1999/05/14
#  with algorithm by clahey
#

# The GIMP -- an image manipulation program
# Copyright (C) 1995 Spencer Kimball and Peter Mattis
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

from PIL import Image

# colortoalpha
# a: (R,G,B,A)の入力値 0-255
# c: 透明にしたい(R,G,B)の値 0-255
def colortoalpha(a, c):
  alpha = [0, 0, 0, a[3]]
  
  if a[0] > c[0]:
    alpha[0] = int((a[0] - c[0]) / (255 - c[0]))
  elif a[0] < c[0]:
    alpha[0] = (c[0] - a[0]) / c[0]
  #else:
  #  alpha[0] = 0

  if a[1] > c[1]:
    alpha[1] = int((a[1] - c[1]) / (255 - c[1]))
  elif a[1] < c[1]:
    alpha[1] = (c[1] - a[1]) / c[1]
  #else:
  #  a[1] = 0

  if a[2] > c[2]:
    alpha[2] = int((a[2] - c[2]) / (255 - c[2]))
  elif a[2] < c[2]:
    alpha[2] = (c[2] - a[2]) / c[2]
  #else:
  #  a[2] = 0

  ret = [0, 0, 0, 0]
  
  if alpha[0] > alpha[1]:
    if alpha[0] > alpha[2]:
      ret[3] = alpha[0]
    else:
      ret[3] = alpha[2]
  else:
    if alpha[1] > alpha[2]:
      ret[3] = alpha[1]
    else:
      ret[3] = alpha[2]

  ret[3] *= 255
  if ret[3] < 1.0: return ret

  ret[0] = int(255 * (a[0] - c[0]) / a[3] + c[0])
  ret[1] = int(255 * (a[1] - c[1]) / a[3] + c[1])
  ret[2] = int(255 * (a[2] - c[2]) / a[3] + c[2])
  ret[3] = int(ret[3] * a[3] / 255)
  
  return ret
      
# main
if __name__ == '__main__':
  import sys

  inFile = sys.argv[1]
  outFile = sys.argv[2]

  src = Image.open(inFile).convert('RGBA')
  dst = Image.new('RGBA', src.size)
  width, height = src.size

  # 透明にしたい色
  color = [255, 255, 255]
  
  for x in range(width):
    for y in range(height):
      r, g, b, a = src.getpixel((x,y))
      r, g, b, a = colortoalpha((r, g, b, a), color)
      dst.putpixel((x,y), (r, g, b, a))

  dst.save(outFile)
