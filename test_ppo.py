import argparse
import numpy as np
import gymnasium as gym
from gymnasium.spaces import Discrete, Box
from abc import ABC,abstractmethod
from itertools import pairwise

class Model(ABC):
    @abstractmethod
    def ffn(self,x):
        raise NotImplementedError

class NumpyMlp(Model):
    def __init__(self, layer_sizes):
        self.W,self.B = [],[]
        for a,b in pairwise(layer_sizes):
            self.W.append(np.random.rand(a,b))
            self.B.append(np.random.rand(b))
        relu = lambda x : np.maximum(x,0)
        def softmax(x):
            e_x = np.exp(x-np.max(x))
            return e_x / e_x.sum(axis=0)
        identity = lambda x : x
        self.A = [relu] * (len(self.W)-1) + [softmax] #[identity]
    def ffn(self,x):
        for w,b,act in zip(self.W,self.B,self.A):
            z = np.dot(x,w) + b
            a = act(z)
            x = a
        return a
    def _ffn(self,x,grad=False):
        Grad = [x] if grad else []
        for w,b,act in zip(self.W,self.B,self.A):
            z = np.dot(x,w) + b
            a = act(z)
            x = a
            if grad:
                Grad.extend([z,a])
        return a,Grad

class TorchMlp(Model):
    def __init__(self, layer_sizes):
        import torch.nn as nn
        layers = []
        for a,b in pairwise(layer_sizes):
            layers.append( nn.Linear(a,b) )
            layers.append( nn.Tanh() )
        layers[-1] = nn.Identity()
        self.nn = nn.Sequential(*layers)

    def ffn(self,x):
        pass

def make_model(type_string, n_inp, n_outp):
    mtype,hs = type_string.split(':')
    hs = list(map(int,hs.split(',')))
    layer_sizes = [n_inp ] + hs + [n_outp]
    print(f'{layer_sizes=}')
    ValidModels = {"np_mlp" : NumpyMlp, "torch_mlp" : TorchMlp}
    return ValidModels.get(mtype,NumpyMlp)(layer_sizes)
    
def make_environment(Args):
    env = gym.make(Args.env)
    assert isinstance(env.observation_space, Box), \
        "This example only works for envs with continuous state spaces."
    assert isinstance(env.action_space, Discrete), \
        "This example only works for envs with discrete action spaces."
    obs_dim = env.observation_space.shape[0]
    n_acts = env.action_space.n
    print(f'created env {Args.env} {obs_dim=} {n_acts=}')
    return env,obs_dim,n_acts

def train_one_epoch(env,actor,critic,batch_size,gamma,lmbda):
    batch_obs = []
    batch_acts = []
    batch_rets = []
    n_acts = env.action_space.n
    observations = env.reset()
    episode_rewards = []
    for i in range(batch_size):
        act_prob = actor.ffn(observations)
        act = np.ranodm.choice(n_acts,act_prob)
        batch_obs.append (observations.copy())
        batch_acts.append(act)

        observations, reward, done, _ = env.step()

def main(Args):
    if Args.seed is not None:
        np.random.seed(Args.seed)
        #torch.manual_seed(Args.seed)
    env,obs_dim,n_acts = make_environment(Args)
    actor  = make_model(Args.actor_model, obs_dim, n_acts)
    critic = make_model(Args.critic_model,obs_dim, n_acts)

    for i in range(Args.num_epochs):
        batch_stats = train_one_epoch(env,actor,critic,batch_size=Args.batch_size,gamma=Args.gamma, lmbda=Args.lmbda)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="proximal policy optimization experiment")
    parser.add_argument("--env","-e",       type=str,   default="CartPole-v1", help="environment name")
    parser.add_argument("--batch_size","-b",type=int,   default="5000", help="number of samples to collect for one epoch")
    parser.add_argument("--num_epochs","-n",type=int,   default="50",   help="number of one epochs")
    parser.add_argument("--actor_model","-a",type=str,  default="np_mlp:32,32",   help="number of one epochs")
    parser.add_argument("--critic_model","-c",type=str, default="np_mlp:16,16",   help="number of one epochs")
    parser.add_argument("--gamma","-g",     type=float, default=0.98,   help="gamma")
    parser.add_argument("--lmbda","-l",     type=float, default=0.95,   help="lambda")
    parser.add_argument('--seed', '-s',     type=int)
    Args = parser.parse_args()
    main(Args)

