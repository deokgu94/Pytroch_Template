import numpy as np
import torch
from torchvision.utils import make_grid
<<<<<<< HEAD
from base.base_trainer_seg import BaseTrainer
from utils import inf_loop, MetricTracker
from tqdm import tqdm
from utils import label_accuracy_score, add_hist


class Trainer_seg(BaseTrainer):
=======
from base import BaseTrainer, BaseTrainer_det
from utils import inf_loop, MetricTracker
from tqdm import tqdm


class Trainer(BaseTrainer):
>>>>>>> 3ac6eebd04a40af0dff8c86ffcf7be84eef72df3
    """
    Trainer class
    """
    def __init__(self, model, criterion, optimizer, config, device,
                 data_set, lr_scheduler=None, len_epoch=None):
<<<<<<< HEAD
        super().__init__(model = model, criterion = criterion,  data_set = data_set, optimizer = optimizer, config = config)
        self.config = config
        self.device = device
        self.data_set = data_set

        self.lr_scheduler = lr_scheduler
        self.do_validation = True

        self.log_step = self.config["log_step"]

    def _train_epoch(self, epoch, kfold, train_loader, val_loader):
=======
        super().__init__(model = model,criterion = criterion, optimizer = optimizer, config = config, data_set = data_set)
        self.config = config
        self.device = device
        self.data_set = data_set
        if len_epoch is None:
            # epoch-based training
            self.len_epoch = len(self.data_set)
        else:
            # iteration-based training
            self.data_set = inf_loop(data_set)
            self.len_epoch = len_epoch

        self.lr_scheduler = lr_scheduler
        self.log_step = int(np.sqrt(self.config["batch_size"]))

        # self.train_metrics = MetricTracker('loss', *[m.__name__ for m in self.metric_ftns], writer=self.writer)
        # self.valid_metrics = MetricTracker('loss', *[m.__name__ for m in self.metric_ftns], writer=self.writer)

    def _train_epoch(self, epoch, train_loader):
>>>>>>> 3ac6eebd04a40af0dff8c86ffcf7be84eef72df3
        """
        Training logic for an epoch

        :param epoch: Integer, current training epoch.
        :return: A log that contains average loss and metric in this epoch.
        """
        self.model.train()
<<<<<<< HEAD
        self.len_epoch = len(train_loader)
        # print(self.len_epoch)

        train_loader.dataset.mode = "train"
        # self.train_metrics.reset()
        hist = np.zeros((11, 11))
        for batch_idx, (images, masks, _) in enumerate(train_loader):
            images = torch.stack(images)       
            masks = torch.stack(masks).long() 
            
            # gpu 연산을 위해 device 할당
            images, masks = images.to(self.device), masks.to(self.device)
            
            # inference
            outputs = self.model(images)
            
            # loss 계산 (cross entropy loss)
            loss = self.criterion(outputs, masks)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            outputs = torch.argmax(outputs, dim=1).detach().cpu().numpy()
            masks = masks.detach().cpu().numpy()
            
            hist = add_hist(hist, masks, outputs, n_class=11)
            acc, acc_cls, mIoU, fwavacc, IoU = label_accuracy_score(hist)
            
            # step 주기에 따른 loss 출력
            if batch_idx % self.log_step == 0 :
                if self.config["save"] : self.logger.debug('Train kfold: {} Epoch: {} {} Loss: {:.6f} mIOU: {:.4f}'.format(
                    kfold,
                    epoch,
                    self._progress(batch_idx, train_loader),
                    loss.item(),
                    mIoU))

            if batch_idx == self.len_epoch:
                break

        log = {"acc": acc,"acc_cls": acc_cls, "mIoU" : mIoU, "fwavacc": fwavacc,}
        if self.do_validation:
            val_log = self._valid_epoch(epoch, kfold, val_loader)
            log.update(**{'val_'+k : v for k, v in val_log.items()})

=======
        print(dir(train_loader))
        train_loader.data_set.mode = "train"
        # self.train_metrics.reset()
        for batch_idx, (data, target, _) in enumerate(data_loader):
            data, target = data.to(self.device), target.to(self.device)

            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()

            self.writer.set_step((epoch - 1) * self.len_epoch + batch_idx)
            # self.train_metrics.update('loss', loss.item())

            if batch_idx % self.log_step == 0 :
                self.logger.debug('Train Epoch: {} {} Loss: {:.6f}'.format(
                    epoch,
                    self._progress(batch_idx),
                    loss.item()))
                self.writer.add_image('input', make_grid(data.cpu(), nrow=8, normalize=True))

            if batch_idx == self.len_epoch:
                break
        # log = self.train_metrics.result()
        log 
>>>>>>> 3ac6eebd04a40af0dff8c86ffcf7be84eef72df3
        if self.lr_scheduler is not None:
            self.lr_scheduler.step()
        return log

<<<<<<< HEAD
    def _valid_epoch(self, epoch, kfold, val_loader):
=======
    def _valid_epoch(self, epoch):
>>>>>>> 3ac6eebd04a40af0dff8c86ffcf7be84eef72df3
        """
        Validate after training an epoch

        :param epoch: Integer, current training epoch.
        :return: A log that contains information about validation
        """
        self.model.eval()
<<<<<<< HEAD
        val_loader.dataset.mode = "val"
        # self.valid_metrics.reset()
        with torch.no_grad():
            n_class = 11
            total_loss = 0
            cnt = 0
            
            hist = np.zeros((11, 11))
            for step, (images, masks, _) in enumerate(val_loader):
                images = torch.stack(images)       
                masks = torch.stack(masks).long()  

                images, masks = images.to(self.device), masks.to(self.device)            
                
                outputs = self.model(images)
                loss = self.criterion(outputs, masks)
                total_loss += loss
                cnt += 1
                
                outputs = torch.argmax(outputs, dim=1).detach().cpu().numpy()
                masks = masks.detach().cpu().numpy()
                
                hist = add_hist(hist, masks, outputs, n_class=11)
            
            acc, acc_cls, mIoU, fwavacc, IoU = label_accuracy_score(hist)
            IoU_by_class = [{classes : round(IoU,4)} for IoU, classes in zip(IoU , ['Backgroud', 'General trash', 'Paper', 'Paper pack', 'Metal', 'Glass', 'Plastic', 'Styrofoam', 'Plastic bag', 'Battery', 'Clothing'])]
            
            avrg_loss = total_loss / cnt
            if self.config["save"] : self.logger.debug('Train kfold: {} Epoch: {} Loss: {:.6f} mIOU: {:.4f}'.format(
                    kfold,
                    epoch,
                    avrg_loss.item(),
                    mIoU))
            if self.config["save"] : self.logger.debug(f'IoU by class : {IoU_by_class}')

            log = {"acc": acc,"acc_cls": acc_cls, "mIoU" : mIoU, "fwavacc": fwavacc, "IoU_by_class": IoU_by_class}
        return log

    def _progress(self, batch_idx, loader):
        base = '[{}/{} ({:.0f}%)]'
        # if hasattr(self.data_loader, 'n_samples'):
        #     current = batch_idx * self.data_loader.batch_size
        #     total = self.data_loader.n_samples
        # else:
        current = batch_idx
        total = len(loader)
        return base.format(current, total, 100.0 * current / total)
=======
        self.valid_metrics.reset()
        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(self.valid_data_loader):
                data, target = data.to(self.device), target.to(self.device)

                output = self.model(data)
                loss = self.criterion(output, target)

                self.writer.set_step((epoch - 1) * len(self.valid_data_loader) + batch_idx, 'valid')
                self.valid_metrics.update('loss', loss.item())
                self.writer.add_image('input', make_grid(data.cpu(), nrow=8, normalize=True))

        # add histogram of model parameters to the tensorboard
        for name, p in self.model.named_parameters():
            self.writer.add_histogram(name, p, bins='auto')
        return self.valid_metrics.result()

    def _progress(self, batch_idx):
        base = '[{}/{} ({:.0f}%)]'
        if hasattr(self.data_loader, 'n_samples'):
            current = batch_idx * self.data_loader.batch_size
            total = self.data_loader.n_samples
        else:
            current = batch_idx
            total = self.len_epoch
        return base.format(current, total, 100.0 * current / total)





class Averager:
    def __init__(self):
        self.current_total = 0.0
        self.iterations = 0.0

    def send(self, value):
        self.current_total += value
        self.iterations += 1

    @property
    def value(self):
        if self.iterations == 0:
            return 0
        else:
            return 1.0 * self.current_total / self.iterations

    def reset(self):
        self.current_total = 0.0
        self.iterations = 0.0

class Trainer_det(BaseTrainer_det):
    """
    Trainer class
    """
    def __init__(self, model, criterion, metric_ftns, optimizer, config, device, transform,
                 data_loader, valid_data_loader=None, lr_scheduler=None, len_epoch=None,):
        super().__init__(model, criterion, metric_ftns, optimizer, config, data_loader, transform)
        self.config = config
        self.device = device
        self.data_loader = data_loader
        if len_epoch is None:
            # epoch-based training
            self.len_epoch = len(self.data_loader)
        else:
            # iteration-based training
            self.data_loader = inf_loop(data_loader)
            self.len_epoch = len_epoch
        self.valid_data_loader = valid_data_loader
        self.do_validation = self.valid_data_loader is not None
        self.lr_scheduler = lr_scheduler
        self.log_step = int((len(data_loader) / self.config["batch_size"]) // 8)

        self.train_metrics = MetricTracker('loss', *[m.__name__ for m in self.metric_ftns], writer=self.writer)
        self.valid_metrics = MetricTracker('loss', *[m.__name__ for m in self.metric_ftns], writer=self.writer)

        self.loss_hist = Averager()
        self.score_threshold = self.config["score_threshold"]

    def _train_epoch(self, epoch, kfold, data_loader):
        """
        Training logic for an epoch

        :param epoch: Integer, current training epoch.
        :return: A log that contains average loss and metric in this epoch.
        """

        self.model.to(self.device)
        self.model.train()
        self.loss_hist.reset()
        self.len_data_set = len(data_loader)
        for batch_idx, (images, targets, *_) in tqdm(enumerate(data_loader)):
            images = torch.stack(images) # bs, ch, w, h - 16, 3, 512, 512
            images = images.to(self.device).float()
            boxes = [target['boxes'].to(self.device).float() for target in targets]
            labels = [target['labels'].to(self.device).float() for target in targets]
            target = {"bbox": boxes, "cls": labels}

            self.optimizer.zero_grad()
            loss, cls_loss, box_loss = self.model(images, target).values()
            loss_value = loss.detach().item()

            self.loss_hist.send(loss_value)

            loss.backward()
            self.optimizer.step()

            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5) # 
            if batch_idx % self.log_step == 0:
                if self.config["save"] : self.logger.debug('Train Epoch, kfold: {} {} {} Loss: {:.6f}'.format(
                    epoch,
                    kfold, 
                    self._progress((batch_idx+1)*self.config["batch_size"]),
                    self.loss_hist.value))

            if batch_idx == self.len_epoch:
                break
        log = {"loss" : self.loss_hist.value}
        return log

        # if self.lr_scheduler is not None:
        #     self.lr_scheduler.step()
        # return log

    def _valid_epoch(self, valid_data_loader):
        """
        Validate after training an epoch

        :param epoch: Integer, current training epoch.
        :return: A log that contains information about validation
        """
        config = get_efficientdet_config(self.config["Net"]["args"]["det_name"])
        config.num_classes = 10
        config.image_size = (512,512)
        
        config.soft_nms = False
        config.max_det_per_image = 40
        
        checkpoint = torch.load(self.is_save_pth_filename, map_location='cpu')
        net = EfficientDet(config, pretrained_backbone=False)

        net.class_net = HeadNet(config, num_outputs=config.num_classes)

        net = DetBenchPredict(net)
        net.load_state_dict(checkpoint)
        net.eval()
        net.to(self.device)
        
        with torch.no_grad():
            new_pred = []
            gt = []
            for images, targets, _, filename in tqdm(valid_data_loader):
                # gpu 계산을 위해 image.to(device)       
                images = torch.stack(images) # bs, ch, w, h 
                images = images.to(self.device).float()
                output = net(images)
                outputs = []
                for out in output:
                    outputs.append({'boxes': out.detach().cpu().numpy()[:,:4], 
                                    'scores': out.detach().cpu().numpy()[:,4], 
                                    'labels': out.detach().cpu().numpy()[:,-1]})  
                for i, output in enumerate(outputs):
                    for box, score, label in zip(output['boxes'], output['scores'], output['labels']):
                        if score > self.score_threshold:
                            new_pred.append([filename[i], int(label), score, box[0]*2, box[2]*2, box[1]*2, box[3]*2])
                for i, target in enumerate(targets):
                    bbox = target["boxes"][i]
                    gt.append([filename[i], int(target["labels"][i]), bbox[1].item(), bbox[3].item(), bbox[0].item(), bbox[2].item()])
            mean_ap, _ = mean_average_precision_for_boxes(gt, new_pred, iou_threshold=0.5)
        return {"mAP" : mean_ap}

    def _save_checkpoint(self, epoch, save_best=False):
        """
        Saving checkpoints

        :param epoch: current epoch number
        :param log: logging information of the epoch
        :param save_best: if True, rename the saved checkpoint to 'model_best.pth'
        """
        if self.config["save"] :
            if save_best:
                filename = str(self.checkpoint_dir / 'model_best-epoch{}.pth'.format(epoch))
                torch.save(self.model.state_dict(), best_path)
                self.logger.info("Saving current best: model_best.pth ...")
            else:
                filename = str(self.checkpoint_dir / 'checkpoint-epoch{}.pth'.format(epoch))
                torch.save(self.model.state_dict(), filename)
                self.logger.info("Saving checkpoint: {} ...".format(filename))
            self.is_save_pth_filename = filename
    
    def _progress(self, batch_idx):
        base = '[{}/{} ({:.0f}%)]'
        # if hasattr(self.len_data_set, 'n_samples'):
        #     current = batch_idx * self.len_data_set
        #     total = self.len_data_set.n_samples
        # else:
        current = batch_idx
        total = self.len_epoch
        return base.format(current, total, 100.0 * current / total)
        
>>>>>>> 3ac6eebd04a40af0dff8c86ffcf7be84eef72df3
