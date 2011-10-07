#
# Copyright 2005,2007 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
import math


#
#           1
# H(s) = -------
#         1 + s
#
# tau is the RC time constant.
# critical frequency: w_p = 1/tau
#
# We prewarp and use the bilinear z-transform to get our IIR coefficients.
# See "Digital Signal Processing: A Practical Approach" by Ifeachor and Jervis
#

class fm_deemph(gr.hier_block2):
    """
    FM Deemphasis IIR filter.
    """
    
			    
    def __init__(self, fs, tau=75e-6):
        """
        @param fs: sampling frequency in Hz
        @type fs: float
        @param tau: Time constant in seconds (75us in US, 50us in EUR)
        @type tau: float
        """
        gr.hier_block2.__init__(self, "fm_deemph",
				gr.io_signature(1, 1, gr.sizeof_float), # Input signature
				gr.io_signature(1, 1, gr.sizeof_float)) # Output signature
				
        w_p = 1/tau
        w_pp = math.tan (w_p / (fs * 2)) # prewarped analog freq

        a1 = (w_pp - 1)/(w_pp + 1)
        b0 = w_pp/(1 + w_pp)
        b1 = b0

        btaps = [b0, b1]
        ataps = [1, a1]

        if 0:
            print "btaps =", btaps
            print "ataps =", ataps
            global plot1
            plot1 = gru.gnuplot_freqz (gru.freqz (btaps, ataps), fs, True)

        deemph = gr.iir_filter_ffd(btaps, ataps)
	self.connect(self, deemph, self)

#
#         1 + s*t1
# H(s) = ----------
#         1 + s*t2
#
# I think this is the right transfer function.
#
#
# This fine ASCII rendition is based on Figure 5-15
# in "Digital and Analog Communication Systems", Leon W. Couch II
#
#
#               R1
#         +-----||------+
#         |             |
#  o------+             +-----+--------o
#         |      C1     |     |
#         +----/\/\/\/--+     \
#                             /
#                             \ R2
#                             /
#                             \
#                             |
#  o--------------------------+--------o
#
# f1 = 1/(2*pi*t1) = 1/(2*pi*R1*C)
#
#         1          R1 + R2
# f2 = ------- = ------------
#      2*pi*t2    2*pi*R1*R2*C
#
# t1 is 75us in US, 50us in EUR
# f2 should be higher than our audio bandwidth.
#
#
# The Bode plot looks like this:
#
#
#                    /----------------
#                   /
#                  /  <-- slope = 20dB/decade
#                 /
#   -------------/
#               f1    f2
#
# We prewarp and use the bilinear z-transform to get our IIR coefficients.
# See "Digital Signal Processing: A Practical Approach" by Ifeachor and Jervis
#

class fm_preemph(gr.hier_block2):
    """
    FM Preemphasis IIR filter.
    """
    def __init__(self, fg, fs, tau1=50e-6, f2):
        """
        @param fg: flow graph
        @type fg: gr.flow_graph
        @param fs: sampling frequency in Hz
        @type fs: float
        @param tau1: Time constant in seconds (75us in US, 50us in EUR)
        @type tau1: float
        @param f2: cutoff frequency in Hz,choose f2 > f1 ( f1 is 2.12KHz in US, 3.2KHz in EUR)
        @type f2: float
        """
        
    tau2=tau1/(2*math.pi*f2*tau1-1)
    w_1=1/tau1
    w_2=1/tau2
    w_p1=math.tan(w_1/(fs*2))
    w_p2=math.tan(w_2/(fs*2))
    b0=(w_p2+1)/(1+w_p1+w_p2)
    b1=(w_p2-1)/(1+w_p1+w_p2)
    a1=(w_p1+w_p2-1)/(w_p1+w_p2+1)
    btaps = [b0,b1]
             ataps = [1,a1]
             if 0:
                    print "btaps =", btaps
                    print "ataps =", ataps
                   global plot2
                    plot2 = gru.gnuplot_freqz (gru.freqz (btaps, ataps), fs, True)
            preemph = gr.iir_filter_ffd(10*btaps, ataps)
    
    gr.hier_block.__init__(self, fg, preemph, preemph)
