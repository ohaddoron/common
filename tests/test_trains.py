import os.path
import pickle

from pl_examples.basic_examples.autoencoder import LitAutoEncoder, MyDataModule
from pytorch_lightning import Trainer, LightningModule

from pl_bolts.models import LitMNIST
from common.loggers import TrainsLogger
from pytorch_lightning.utilities.cli import LightningCLI
from torch.utils.data import random_split, DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST, FashionMNIST


class LightningTestModule(LitAutoEncoder):
    def __init__(
            self,
            batch_size: int = 32,
    ):
        super().__init__()
        dataset = FashionMNIST(os.path.join(os.path.dirname(__file__), '../resources'), train=True, download=True,
                               transform=transforms.ToTensor())
        self.mnist_test = FashionMNIST(os.path.join(os.path.dirname(__file__), '../resources'), train=True,
                                       download=True,
                                       transform=transforms.ToTensor())
        self.mnist_train, self.mnist_val = random_split(dataset, [55000, 5000])
        self.batch_size = batch_size

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size)

    def predict_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size)


def test_trains_logger(tmpdir):
    """Verify that basic functionality of TRAINS logger works."""

    # model = LitMNIST(data_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources')))
    model = LightningTestModule()
    TrainsLogger.set_bypass_mode(True)
    TrainsLogger.set_credentials(api_host='http://integration.trains.allegro.ai:8008',
                                 files_host='http://integration.trains.allegro.ai:8081',
                                 web_host='http://integration.trains.allegro.ai:8080', )
    logger = TrainsLogger(project_name="lightning_log",
                          task_name="pytorch lightning test")

    trainer = Trainer(
        default_root_dir=tmpdir,
        max_epochs=1,
        limit_train_batches=0.05,
        logger=logger,
    )
    result = trainer.fit(model)

    print('result finished')
    logger.finalize()


def test_trains_pickle(tmpdir):
    """Verify that pickling trainer with TRAINS logger works."""
    # hparams = tutils.get_default_hparams()
    # model = LightningTestModel(hparams)
    TrainsLogger.set_bypass_mode(True)
    TrainsLogger.set_credentials(api_host='http://integration.trains.allegro.ai:8008',
                                 files_host='http://integration.trains.allegro.ai:8081',
                                 web_host='http://integration.trains.allegro.ai:8080', )
    logger = TrainsLogger(project_name="lightning_log",
                          task_name="pytorch lightning test")

    trainer = Trainer(
        default_root_dir=tmpdir,
        max_epochs=1,
        logger=logger
    )
    pkl_bytes = pickle.dumps(trainer)
    trainer2 = pickle.loads(pkl_bytes)
    trainer2.logger.log_metrics({"acc": 1.0})
    trainer2.logger.finalize()
    logger.finalize()
