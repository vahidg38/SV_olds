#by Vahid
#https://www.deeplearningwizard.com/deep_learning/practical_pytorch/pytorch_autoencoder/
from models import *
from arguments import *
from sklearn.decomposition import PCA

args = get_args()


np.random.seed(4)
path=args.path

"""# **Data loading**"""
train_data, test_data = data_loading(mat_file=path, train_test_ratio=4)

mu, sigma = 0, 0.1
noise = np.random.normal(mu, sigma, len(train_data)*5).reshape(-1,5)

train_noisy= train_data + noise



# Generating  train and real_test , and noisy train dataframes
train_ori, test_ori, train_n_ori = create_dataframe(train_data), create_dataframe(test_data), create_dataframe(train_noisy)
print(train_ori.describe())
print(test_ori.describe())
print(train_n_ori.describe())

#normalizing the data

train, test, train_n = normalize(train_ori, test_ori, train_n_ori)
# print(train.describe())
# print(test.describe())
# print(train_n.describe())

# Generating  faulty_test dataframe
test_faulty= fault_generation(test.copy(), type=args.failure, sensor=args.fsensor, magnitude=args.fmagnitude, start=args.fstart, stop=args.fstop)



#
args.model="MAE"
MAE= model(args, train, train_n, test, test_faulty)
#MAE.optimization()
MAE.train_model()
MAE.reconstruct(train,train_ori, description="train")
z, x,e= MAE.reconstruct(test,test_ori ,description="test")
print(f"MSE for {args.model}:  {MSE(z,x)}")
print(f"RR for {args.model}:  {RR(z,x)}")
#z, x, ee=MAE.reconstruct(test_faulty,test_ori ,description=args.failure)
#print(f"MSE for {args.model}:  {MSE(z,x)}")
#print(f"RR for {args.model}:  {RR(z,x)}")

#for i in range(len(e["error"])//10):
#for i in range(args.pstart,args.pstop):
# for i in range(args.fstart-10, args.fstart+10):
#     print(i)
#     print(f"error sum: {np.sum(np.absolute(ee['error'][i][0]))}")
#     print(f"error: {ee['error'][i][0]}")
#     print(f"recons: {z.values[i]}")
#     print(f" Input: {x.values[i]}")
#     print("###############################")



args.model="AE"
AE= model(args, train, train_n, test, test_faulty)
#AE.optimization()
AE.train_model()
AE.reconstruct(train,train_ori, description="train")
z, x,e= AE.reconstruct(test, test_ori, description="test")
print(f"MSE for {args.model}:  {MSE(z,x)}")
print(f"RR for {args.model}:  {RR(z,x)}")
# z,x,e=AE.reconstruct(test_faulty,test_ori ,description=args.failure)
# print(f"MSE for {args.model}:  {MSE(z,x)}")
# print(f"RR for {args.model}:  {RR(z,x)}")


args.model="DAE"
DAE= model(args, train, train_n, test, test_faulty)
#DAE.optimization()
DAE.train_model()
DAE.reconstruct(train,train_ori, description="train")
z, x,e= DAE.reconstruct(test,test_ori, description="test")
print(f"MSE for {args.model}:  {MSE(z,x)}")
print(f"RR for {args.model}:  {RR(z,x)}")
# z,x,e=DAE.reconstruct(test_faulty,test_ori ,description=args.failure)
# print(f"MSE for {args.model}:  {MSE(z,x)}")
# print(f"RR for {args.model}:  {RR(z,x)}")

args.model="VAE"
VAE= model(args, train, train_n, test, test_faulty)
#VAE.optimization()
VAE.train_model()
VAE.reconstruct(train,train_ori ,description="train")
z, x,e= VAE.reconstruct(test,test_ori, description="test")
print(f"MSE for {args.model}:  {MSE(z,x)}")
print(f"RR for {args.model}:  {RR(z,x)}")
# z,x,e=VAE.reconstruct(test_faulty,test_ori ,description=args.failure)
# print(f"MSE for {args.model}:  {MSE(z,x)}")
# print(f"RR for {args.model}:  {RR(z,x)}")

args.model="MVAE"
MVAE= model(args, train, train_n, test, test_faulty)
#MVAE.optimization()
MVAE.train_model()
MVAE.reconstruct(train,train_ori, description="train")
z, x,e= MVAE.reconstruct(test, test_ori, description="test")
print(f"MSE for {args.model}:  {MSE(z,x)}")
print(f"RR for {args.model}:  {RR(z,x)}")
# z,x,e=MVAE.reconstruct(test_faulty,test_ori ,description=args.failure)
# print(f"MSE for {args.model}:  {MSE(z,x)}")
# print(f"RR for {args.model}:  {RR(z,x)}")



