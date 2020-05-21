import unittest

import torch

from torch_scae.configs import mnist_config
from torch_scae.object_decoder import CapsuleLayer, CapsuleObjectDecoder
from torch_scae.part_decoder import TemplateBasedImageDecoder, TemplateGenerator
from torch_scae.part_encoder import CNNEncoder, CapsuleImageEncoder
from torch_scae.set_transformer import SetTransformer
from torch_scae.stacked_capsule_auto_encoder import SCAE


class SCAETestCase(unittest.TestCase):
    def test_scae(self):
        config = mnist_config

        cnn_encoder = CNNEncoder(**config.pcae_cnn_encoder)
        part_encoder = CapsuleImageEncoder(
            encoder=cnn_encoder,
            **config.pcae_encoder
        )

        template_generator = TemplateGenerator(**config.pcae_template_generator)
        part_decoder = TemplateBasedImageDecoder(**config.pcae_decoder)

        obj_encoder = SetTransformer(**config.ocae_encoder_set_transformer)

        obj_decoder_capsule = CapsuleLayer(**config.ocae_decoder_capsule)
        obj_decoder = CapsuleObjectDecoder(obj_decoder_capsule)

        scae = SCAE(
            part_encoder=part_encoder,
            template_generator=template_generator,
            part_decoder=part_decoder,
            obj_encoder=obj_encoder,
            obj_decoder=obj_decoder,
            **config.scae
        )

        with torch.no_grad():
            batch_size = 24
            image = torch.rand(batch_size, *config.image_shape)
            label = torch.randint(0, config.n_classes, (batch_size,))
            reconstruction_target = image

            result = scae(image=image,
                          label=label,
                          reconstruction_target=reconstruction_target)

            # print(result)
