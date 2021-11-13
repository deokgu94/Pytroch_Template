import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score # https://towardsdatascience.com/confusion-matrix-for-your-multi-class-machine-learning-model-ff9aa3bf7826


num_class = 18

def accuracy(output, target):
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        assert pred.shape[0] == len(target)
        correct = 0
        correct += torch.sum(pred == target).item()
    # print(f"Accuracy : {correct / len(target)}")
    # print(f"sklearn.metrics accuracy_score: {accuracy_score(pred.cpu(), target.cpu())}")
    return correct / len(target)

def top_k_acc(output, target, k=3):
    with torch.no_grad():
        pred = torch.topk(output, k, dim=1)[1]
        assert pred.shape[0] == len(target)
        correct = 0
        for i in range(k):
            correct += torch.sum(pred[:, i] == target).item()
    return correct / len(target)

def f1_scores(output, target, num= num_class, is_training=False):
    """
        2 * (precision * recall) / (precision + recall)
        ㄴ precision() : 정미도
        ㄴ recall : 재현률
    """
    with torch.no_grad():
        assert output.shape[0] == len(target)
        if target.ndim == 2:
            target = target.argmax(dim=1)
        pred = torch.argmax(output, dim=1)

        tp = (target * pred).sum().to(torch.float32)
        tn = ((num - target) * (num - pred)).sum().to(torch.float32)
        fp = ((num - target) * pred).sum().to(torch.float32)
        fn = (target * (num - pred)).sum().to(torch.float32)
        
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        # print(f"F1 score : {2* (precision*recall) / (precision + recall)}")
        # print(f"sklearn.metrics f1_score: {f1_score(pred.cpu(), target.cpu(), average='macro', zero_division = 0)}")
        
        f1 = 2* (precision*recall) / (precision + recall) 
        f1.requires_grad = False
    return f1

def specificity(output, target, num= num_class): # check
    with torch.no_grad():
        assert output.shape[0] == len(target)
        if target.ndim == 2:
            target = target.argmax(dim=1)
        pred = torch.argmax(output, dim=1)    
        tn = ((num - target) * (num - pred)).sum().to(torch.float32)
        fp = ((num - target) * pred).sum().to(torch.float32)
        # print(f"Specificity : {tn/(tn+fp)}")
        specificity = tn/(tn+fp)
    return specificity

def recall(output, target, num= num_class):
    with torch.no_grad():
        assert output.shape[0] == len(target)
        if target.ndim == 2:
            target = target.argmax(dim=1)
        pred = torch.argmax(output, dim=1)    
        tp = (target * pred).sum().to(torch.float32)
        fn = (target * (num - pred)).sum().to(torch.float32)
        recall = tp / (tp + fn)
        # print(f"Sensitivity(Recall) : { tp / (tp + fn)}")
        # print(f"sklearn.metrics recall_score: {recall_score(pred.cpu(), target.cpu(), average='macro', zero_division = 0)}")
    return recall

def precision(output, target, num= num_class):
    with torch.no_grad():
        assert output.shape[0] == len(target)
        if target.ndim == 2:
            target = target.argmax(dim=1)
        pred = torch.argmax(output, dim=1)    
        tp = (target * pred).sum().to(torch.float32)
        fp = ((num - target) * pred).sum().to(torch.float32)
        precision = tp / (tp + fp)
        # print(f"precision : {tp / (tp + fp)}")
        # print(f"sklearn.metrics precision_score: {precision_score(pred.cpu(), target.cpu(), average='macro', zero_division = 0)}")
    return precision

def megative_value(output, target, num= num_class): # check
    with torch.no_grad():
        assert output.shape[0] == len(target)
        if target.ndim == 2:
            target = target.argmax(dim=1)
        pred = torch.argmax(output, dim=1)    
        tn = ((num - target) * (num - pred)).sum().to(torch.float32)
        fn = (target * (num - pred)).sum().to(torch.float32)
        # print(f"Negative predicable value : {tn/(tn+fn)}")
        megative_value = tn/(tn+fn)
    return megative_value