// This file is part of royalUr.
// Copyright (C) 2018 Joseph Heled.
// Author: Joseph Heled <jheled@gmail.com>
// See the files LICENCE and gpl.txt for copying conditions.
//

#include <Python.h>
#undef NDEBUG
#include <cassert>
//#include <iostream>
//using std::cerr;
//using std::endl;

int bmap[20][20];

int binomial(int n, int k)
{
  if( n < k )  return 0;
  if( k == 0 || n == k ) return 1;
  return binomial(n-1,k) + binomial(n-1,k-1);
}

void initm(void) {
  for(int n = 0; n < 20; ++n) {
    for(int k = 0; k < 20; ++k) {
      bmap[n][k] = binomial(n,k);
    }
  }
}
  
inline int
sum(int const a[], uint const n) {
  int s = 0;
  for(uint k = 0; k < n; ++ k) {
    s += a[k];
  }
  return s;
}

uint
bitsIndex(int const bits[], int k, uint const N)
{
  int i = 0, n = N;
  for(uint j = 0; j < N; ++j) {
    if( bits[j] ) {
      i += bmap[n-1][k];
      k -= 1;
    }
    n -= 1;
  }
  return i;
}

void i2bits(int bits[], uint i, int k, int N)
{
  int j;
  for(j = 0; j < N; ++j) {
    bits[j] = 0;
  }
  j = 0;
  while( N > 0 ) {
    uint const bnk = bmap[N-1][k];
    if( i >= bnk ) {
      bits[j] = 1;
      i -= bnk;
      k -= 1;
    }
    N -= 1;
    j += 1;
  }
}

uint const GR_OFF = 14;
uint const RD_OFF = 21;


static PyObject*
board2Index(PyObject*, PyObject* args)
{
  PyObject* pyBoard;
  PyObject* spMap;
  PyObject* pSums;
  
  if( !PyArg_ParseTuple(args, "OOO", &pyBoard, &spMap, &pSums) ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }

  if( !(PySequence_Check(pyBoard) && PySequence_Size(pyBoard) == 22) ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }

  if( !( PyDict_Check(spMap) && PyDict_Check(pSums) ) ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }
  
  int b[22];
  PyObject** s = &PyList_GET_ITEM(pyBoard, 0);
  for(uint k = 0; k < 22; ++k) {
    b[k] = PyInt_AsLong(s[k]);
  }
  
  int const gOff = b[GR_OFF];
  int const rOff = b[RD_OFF];
  
  int const gSafe[6] = {b[0],b[1],b[2],b[3],b[12],b[13]};
  uint const m = sum(gSafe, 6);
  int const partSafeG = bitsIndex(gSafe, m, 6);
  int bits[14];
  for(uint k = 4; k < 12; ++k) {
    bits[k-4] = b[k] == 1;
  }
  int const smb = sum(bits, 8);
  int const gStrip = bitsIndex(bits, smb, 8);
  int const gMen = smb + m;
  
  for(uint k = 15; k < 19; ++k) {
    bits[k-15] = b[k] == -1;
  }
  
  uint nb = 4;
  for(uint k = 4; k < 12; ++k) {
    if( b[k] == 1 ) {
      continue;
    }
    bits[nb] = b[k] == -1;
    nb += 1;
  }
  for(uint k = 19; k < 21; ++k, ++nb) {
    bits[nb] = b[k] == -1;
  }
  int const rMen = sum(bits, nb);
  int const partR = bitsIndex(bits, rMen, nb);
  
  int const gHome = 7 - (gMen + gOff);
  int const rHome = 7 - (rMen + rOff);

  PyObject* t = PyTuple_New(4);
  PyTuple_SET_ITEM(t, 0, PyInt_FromLong(gOff));
  PyTuple_SET_ITEM(t, 1, PyInt_FromLong(rOff));
  PyTuple_SET_ITEM(t, 2, PyInt_FromLong(gHome));
  PyTuple_SET_ITEM(t, 3, PyInt_FromLong(rHome));
  
  PyObject* const pyi0 = PyDict_GetItem(spMap, t);     
  Py_DECREF(t);
  
  if( ! pyi0 ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }
    
  long const i0 = PyInt_AsLong(pyi0);

  t = PyTuple_New(2);
  PyTuple_SET_ITEM(t, 0, PyInt_FromLong(gMen));
  PyTuple_SET_ITEM(t, 1, PyInt_FromLong(rMen));

  PyObject* const pyps = PyDict_GetItem(pSums, t);     assert(pyps);
  Py_DECREF(t);
  
  if( ! PySequence_Check(pyps) ) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  long const i1 = PyInt_AsLong(PyList_GET_ITEM(pyps, m));
  long const i2 = partSafeG * bmap[8][gMen - m] + gStrip;
  long const i3 = i2 * bmap[14 - (gMen-m)][rMen] + partR;
  
  return PyInt_FromLong(i0 + i1 + i3);
}

static PyObject*
index2Board(PyObject*, PyObject* args)
{
  PyObject *pi, *a0, *a1, *a2, *a3;
  PyObject *pSums;

  if( !PyArg_ParseTuple(args, "OOOOOO", &pi, &a0, &a1, &a2, &a3, &pSums) ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }
  uint index = PyInt_AsLong(pi);
  uint
    gOff = PyInt_AsLong(a0),
    rOff = PyInt_AsLong(a1),
    gHome = PyInt_AsLong(a2),
    rHome = PyInt_AsLong(a3);
  
  uint gMen = 7 - (gOff + gHome), rMen = 7 - (rOff + rHome);
  PyObject* t = PyTuple_New(2);
  PyTuple_SET_ITEM(t, 0, PyInt_FromLong(gMen));
  PyTuple_SET_ITEM(t, 1, PyInt_FromLong(rMen));

  PyObject* const pyps = PyDict_GetItem(pSums, t);     assert(pyps && PySequence_Check(pyps));
  Py_DECREF(t);

  uint const plen = PySequence_Length(pyps);
  
  PyObject** ps = &PyList_GET_ITEM(pyps, 0);
  if( index >= PyInt_AsLong(ps[plen-1]) ) {
    PyErr_SetString(PyExc_ValueError, "Index invalid");
    return 0;
  }
    
  int m = 0;
  while( ! ( PyInt_AsLong(ps[m]) <= index && index < PyInt_AsLong(ps[m+1]) ) ) {
    m += 1;
  }
  index -= PyInt_AsLong(ps[m]);
    
  uint u = bmap[14 - (gMen-m)][rMen];
  uint i2 = index / u;
  uint partR = index - i2 * u;
  u = bmap[8][gMen - m];
  uint partSafeG = i2 / u;
  uint gStrip = i2 - u * partSafeG;

  int b[22] = {0};
  b[14] = gOff;
  b[21] = rOff;
  
  i2bits(b, partSafeG, m ,6);
  b[12] = b[4];
  b[13] = b[5];
  b[4] = b[5] = 0;
  
  i2bits(b + 4, gStrip, gMen - m, 8);
  
  int bOther[14 - (gMen-m)];
  i2bits(bOther, partR, rMen, 14 - (gMen-m));

  int i;
  for(i = 0; i < 4; ++i) {
    b[15+i] = -bOther[i];
  }
  for(int k = 4; k < 12; ++k) {
    if( b[k] == 0 ) {
      if( bOther[i] ) {
	b[k] = -1;
      }
      i += 1;
    }
  }
  b[19] = -bOther[i];
  b[20] = -bOther[i+1];

  PyObject* pyb = PyList_New(22);
  for(i = 0; i < 22; ++i) {
    PyList_SET_ITEM(pyb, i, PyInt_FromLong(b[i]));
  }
  return pyb;

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef irMethods[] =
{
  {"board2Index",  board2Index, METH_VARARGS, ""},
  
  {"index2Board",  index2Board, METH_VARARGS, ""},
  
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initirogaur(void)
{
  initm();
  /*PyObject* m = */ Py_InitModule("irogaur", irMethods);
}

