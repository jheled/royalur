## This file is part of royalUr.
## Copyright (C) 2018 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#
from __future__ import division

import random

from royalur.humanStrategies import strategies, chainFilt, nicks
from royalur.play import pitStrategies

# The "genes" are integers [0-nPrinciples), and the genome is a list of unique genes.
#
# Mutations:
# Random genome: a random sequence of genes at some length.
# Mutated one gene: add, delete and mutate: Add a gene at a random spot, delete a gene, change a
#                    gene into another gene. Transpose two genes. 
# Combine genomes: concatenate two genomes (deleting duplications).

# Number of matches between two players. Small but speed matters, and the overall performance is
# judged by the total against the pool, so it is sufficient.
#
N = 500

# How many generations to run
nGenerations = 5000

def randomGenome(genePool) :
  n = len(genePool)
  p = 2./(n-2)
  if p >= 1:
    p = 1./n

  l = 1
  while l < n and random.random() > p:
    l += 1
  return random.sample(genePool, l)

def mutateGenome(genome, genePool) :
  p = random.random()
  genome = list(genome)
  if p < 0.3 and len(genome) < len(genePool):
    # mutate
    k = random.randint(0, len(genome)-1)
    g = random.choice(list(set(genePool) - set(genome[:k] + genome[k+1:])))
    genome[k] = g
  elif p < 0.5 and len(genome) > 1:
    # transpose
    k = random.randint(0, len(genome)-2)
    genome[k:k+2] = [genome[k+1],genome[k]]
  elif p < 0.75:
    # add
    k = random.randint(0, len(genome))
    cans = list(set(genePool) - set(genome))
    if not cans:
      return None
    g = random.choice(cans)
    genome.insert(k, g)
  else:
    # delete
    k = random.randint(0, len(genome)-1)
    genome.pop(k)

  assert len(set(genome)) == len(genome)
  return genome
    
def combineGenomes(genome1, genome2, genePool) :
  nonDups = set(genome2) - set(genome1)
  ng = list(genome1) + [g for g in genome2 if g in nonDups]
  assert len(set(ng)) == len(ng)
  return ng

def newGenome(genomePool, genePool) :
  p = random.random()
  if p < 1./len(genePool) :
    return randomGenome(genePool)
  if p < 1./len(genePool) + 0.75 * (1 - (1./len(genePool))) :
    return mutateGenome(random.choice(genomePool), genePool)
  else :
    g1,g2 = random.sample(genomePool, 2)
    return combineGenomes(g1, g2, genePool)

def name2nick(k) :
  if k == "random": return k
  return nicks[[s.__name__ for s in strategies].index(k)]
    
def genome2Filt(genome) :
  s = [strategies[g] for g in genome]
  f = lambda m : chainFilt(m, s)
  f.__name__ = ";".join([name2nick(x.__name__) for x in s])
  return f

def main():
  genePool = range(len(strategies))
  genomePool = []
  while len(genomePool) < len(strategies) :
    g = tuple(randomGenome(genePool))
    if g not in set(genomePool) :
      genomePool.append(g)

  discarded = set()
  outed = list()

  scores = dict([(g,dict()) for g in genomePool])

  for g in genomePool:
    fg = genome2Filt(g)
    for x in genomePool:
      if x == g:
        continue

      if x not in scores[g]:
        assert g not in scores[x]
        fx = genome2Filt(x)
        wx,wy = pitStrategies(fg, fx, N)
        scores[g][x] = wx
        scores[x][g] = wy
        print(fg.__name__,fx.__name__,wx,wy)

  print(sorted([(sum(scores[g].values()),g) for g in scores]))

  for _ in range(nGenerations):
    while True:
      ng = newGenome(genomePool, genePool)
      if not ng:
        continue
      ng = tuple(ng)
      if ng not in discarded and ng not in set(genomePool) :
        break

    ngs = dict()    
    fng = genome2Filt(ng)
    for g in genomePool:
      fg = genome2Filt(g)
      wx,wy = pitStrategies(fng, fg, N)
      ngs[g] = (wx,wy)
      print(fng.__name__,fg.__name__,wx,wy)

    ngScore = sum([wx for wx,wy in ngs.values()])
    print(ng, ngScore)
    sl = sorted([(sum(scores[g].values()) + ngs[g][1],g) for g in genomePool])
    for sc,g in sl:
      if sc < ngScore:
        print("accepted,", g, "out.")
        discarded.add(g)
        outed.append(g)

        del ngs[g]
        del scores[g]
        for d in scores :
          del scores[d][g]
          scores[d][ng] = ngs[d][1]
        scores[ng] = dict([(x,ngs[x][0]) for x in ngs])

        genomePool.pop(genomePool.index(g))
        genomePool.append(ng)
        ng = None
        break
    if ng :
      discarded.add(ng)
    print(sorted([(sum(scores[g].values()),g) for g in scores]))

if __name__ == "__main__":
  main()
    
