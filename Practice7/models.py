# This file contains the models used for both parts of the assignment:
#
#   - DCGenerator       --> Used in the vanilla GAN in Part A
#   - CycleGenerator    --> Used in the CycleGAN in Part B
#   - DCDiscriminator   --> Used in both the vanilla GAN and CycleGAN (Parts A and B)
#
# For the assignment, you are asked to create the architectures of these three networks by
# filling in the __init__ methods in the DCGenerator, CycleGenerator, and DCDiscriminator classes.


import pdb
import torch
import torch.nn as nn
import torch.nn.functional as F


def deconv(in_channels, out_channels, kernel_size, stride=2, padding=1, batch_norm=True):
    """Creates a transposed-convolutional layer, with optional batch normalization.
    """
    layers = []
    layers.append(nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, bias=False))
    if batch_norm:
        layers.append(nn.BatchNorm2d(out_channels))
    return nn.Sequential(*layers)


def conv(in_channels, out_channels, kernel_size, stride=2, padding=1, batch_norm=True, init_zero_weights=False):
    """Creates a convolutional layer, with optional batch normalization.
    """
    layers = []
    conv_layer = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride,
                           padding=padding, bias=False)
    if init_zero_weights:
        conv_layer.weight.data = torch.randn(out_channels, in_channels, kernel_size, kernel_size) * 0.001
    layers.append(conv_layer)

    if batch_norm:
        layers.append(nn.BatchNorm2d(out_channels))
    return nn.Sequential(*layers)


class DCGenerator(nn.Module):
    def __init__(self, noise_size, conv_dim):
        super(DCGenerator, self).__init__()
        self.conv_dim = conv_dim
        ###########################################
        ##   FILL THIS IN: CREATE ARCHITECTURE   ##
        ###########################################
        ############## TODO #######################
        self.linear_bn = deconv(in_channels=noise_size, out_channels=128, kernel_size=3)
        self.upconv1 = deconv(in_channels=128, out_channels=64, kernel_size=5)
        self.upconv2 = deconv(in_channels=64, out_channels=32, kernel_size=5)
        self.upconv3 = deconv(in_channels=32, out_channels=3, kernel_size=5, batch_norm=False)


def forward(self, z):
        """Generates an image given a sample of random noise.

            Input
            -----
                z: BS x noise_size x 1 x 1   -->  16x100x1x1            

            Output
            ------
                out: BS x channels x image_width x image_height  -->  16x3x32x32
        """
        ##############################################
        ################TODO##########################
        ################# Complete this forward method using deconv block code provided above ######
        batch_size = z.size(0)
        out = F.relu(self.linear_bn(z)).view(-1, self.conv_dim * 4, 4, 4)  # BS x 128 x 4 x 4
        out = F.relu(self.upconv1(out))  # BS x 64 x 8 x 8
        out = F.relu(self.upconv2(out))  # BS x 32 x 16 x 16
        out = F.tanh(self.upconv3(out))  # BS x 3 x 32 x 32

        out_size = out.size()
        if out_size != torch.Size([batch_size, 3, 32, 32]):
            raise ValueError("expect {} x 3 x 32 x 32, but get {}".format(batch_size, out_size))
        return out



class ResnetBlock(nn.Module):
    def __init__(self, conv_dim):
        super(ResnetBlock, self).__init__()
        self.conv_layer = conv(in_channels=conv_dim, out_channels=conv_dim, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        ############## TODO##############
        ###### Complete forward method###
        #################################
        out = x + self.conv_layer(x)
        return out


class CycleGenerator(nn.Module):
    """Defines the architecture of the generator network.
       Note: Both generators G_XtoY and G_YtoX have the same architecture in this assignment.
    """

    def __init__(self, conv_dim=64, init_zero_weights=False):
        super(CycleGenerator, self).__init__()

        ###########################################
        ##   FILL THIS IN: CREATE ARCHITECTURE   ##
        ###########################################

        # Define the encoder part of the generator (that extracts features from the input image)
        self.conv1 = conv(3, conv_dim, 5, init_zero_weights=init_zero_weights)
        self.conv2 = conv(conv_dim, conv_dim * 2, 5, init_zero_weights=init_zero_weights)

        # # 2. Define the transformation part of the generator
        # self.resnet_block = ResnetBlock(conv_dim * 2)
        #
        # # 3. Define the decoder part of the generator (that builds up the output image from features)
        # self.upconv1 = deconv(conv_dim * 2, conv_dim, 5)
        # self.upconv2 = conv(conv_dim, 3, 5, batch_norm=False)

    def forward(self, x):
        """Generates an image conditioned on an input image.

            Input
            -----
                x: BS x 3 x 32 x 32

            Output
            ------
                out: BS x 3 x 32 x 32
        """
        ################# Complete this forward method using conv, resnet and deconv blocks provided above ######
        batch_size = x.size(0)

        out = F.relu(self.conv1(x))  # BS x 32 x 16 x 16
        out = F.relu(self.conv2(out))  # BS x 64 x 8 x 8

        # out = F.relu(self.resnet_block(out))  # BS x 64 x 8 x 8
        #
        # out = F.relu(self.upconv1(out))  # BS x 32 x 16 x 16
        # out = F.tanh(self.upconv2(out))  # BS x 3 x 32 x 32

        out_size = out.size()
        if out_size != torch.Size([batch_size, 3, 32, 32]):
            raise ValueError("expect {} x 3 x 32 x 32, but get {}".format(batch_size, out_size))

        return out


class DCDiscriminator(nn.Module):
    """Defines the architecture of the discriminator network.
       Note: Both discriminators D_X and D_Y have the same architecture in this assignment.
    """

    def __init__(self, conv_dim=64):
        super(DCDiscriminator, self).__init__()

        ###########################################
        ##   FILL THIS IN: CREATE ARCHITECTURE   ##
        ###########################################
        self.conv1 = conv(in_channels=3, out_channels=32, kernel_size=5, stride=2, padding=2)
        self.conv2 = conv(in_channels=32, out_channels=64, kernel_size=5, stride=2, padding=2)
        self.conv3 = conv(in_channels=64, out_channels=128, kernel_size=5, stride=2, padding=2)
        self.conv4 = conv(in_channels=128, out_channels=1, kernel_size=4, stride=2, padding=0, batch_norm=False)

    def forward(self, x):
        ################# Complete this forward method using conv block code provided above ######

        batch_size = x.size(0)

        out = F.relu(self.conv1(x))  # BS x 64 x 16 x 16
        out = F.relu(self.conv2(out))  # BS x 64 x 8 x 8
        out = F.relu(self.conv3(out))  # BS x 64 x 4 x 4

        out = self.conv4(out).squeeze()
        out_size = out.size()
        if out_size != torch.Size([batch_size, ]):
            raise ValueError("expect {} x 1, but get {}".format(batch_size, out_size))
        return out
