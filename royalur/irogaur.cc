// This file is part of royalUr.
// Copyright (C) 2018 Joseph Heled.
// Author: Joseph Heled <jheled@gmail.com>
// See the files LICENCE and gpl.txt for copying conditions.
//

#include <Python.h>
#undef NDEBUG
#include <cassert>
#include <cmath>

#include <iostream>
using std::cerr;
using std::endl;

int bmap[20][20];

static const char
z85s[] = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#";
static int rz85[256];

static int
binomial(int n, int k)
{
  if( n < k )  return 0;
  if( k == 0 || n == k ) return 1;
  return binomial(n-1,k) + binomial(n-1,k-1);
}

static void
initm(void)
{
  for(int n = 0; n < 20; ++n) {
    for(int k = 0; k < 20; ++k) {
      bmap[n][k] = binomial(n,k);
    }
  }
  {
    uint k = 0;
    for(char const& c : z85s) {
      rz85[static_cast<uint>(c)] = k;
      ++k;
    }
  }
}
  
inline int
sum(int const a[], uint const n)
{
  int s = 0;
  for(uint k = 0; k < n; ++ k) {
    s += a[k];
  }
  return s;
}

static uint
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

static void
i2bits(int bits[], uint i, int k, int N)
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
}

static unsigned long
a2b(const char* s)
{
  unsigned long l = 0;
  for(int i = 4; i >= 0; --i) {
    l = l*85 + rz85[static_cast<uint>(s[i])];
  }
  
  assert( (l & (0x1 << 31)) == 0);
  return l;
}

static void
b2a(bool s[31], char a[5])
{
  unsigned long l = 0;
  for(uint i = 0; i < 31; ++i) {
    l = 2*l + s[i];
  }
  
  for(uint i = 0; i < 5; ++i) {
    uint const c = l % 85;
    a[i] = z85s[c];
    l = (l - c) / 85;
  }
}

inline uint
unpack(unsigned long l, uint start, uint len)
{
  l = l >> (31 - (start + len));
  l &= (0x1 << len) - 1;
  return l;
}

inline bool
ubit(unsigned long l, uint i)
{
  return l & (0x1 << (30 - i));
}

static PyObject*
code2Board(PyObject*, PyObject* args)
{
  const char* e;
  if( !PyArg_ParseTuple(args, "s", &e) ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }
  
  int board[22] = {0};
  unsigned long l = a2b(e);
  uint atHome(unpack(l, 0, 3)), oAtHome(unpack(l, 9, 3));        assert(atHome <= 7 && oAtHome <= 7);
  
  {
    int b[6] = {3,4,5,6,7,8};
    int k[6] = {0,1,2,3,12,13};
    for(uint i = 0; i < 6; ++i) {
      if( ubit(l, b[i]) ) {
  	board[k[i]] = 1;
      }
    }
  }
  {
    int b[6] = {12,13,14,15,16,17};
    int k[6] = {15,16,17,18,19,20};
    for(uint i = 0; i < 6; ++i) {
      if( ubit(l, b[i]) ) {
  	board[k[i]] = -1;
      }
    }
  }
  
  uint mid = unpack(l, 18, 13);                     assert( mid < std::pow(3,8) );
  for(int i = 11; i > 3; --i) {
    uint const x = mid % 3;
    board[i] = x - 1;
    mid = (mid - x) / 3;
  }
  
  uint n = 0;
  for(uint k = 0; k < 14; ++k) {
    n += board[k] == 1;
  }
  board[14] = 7 - (atHome + n);
  
  n = 0;
  for(uint k = 15; k < 19; ++k) {
    n += board[k] == -1;
  }
  for(uint k = 4; k < 12; ++k) {
    n += board[k] == -1;
  }
  for(uint k = 19; k < 21; ++k) {
    n += board[k] == -1;
  }
  
  board[21] = 7 - (oAtHome + n);
  
  PyObject* pyb = PyList_New(22);
  for(uint i = 0; i < 22; ++i) {
    PyList_SET_ITEM(pyb, i, PyInt_FromLong(board[i]));
  }
  return pyb;
}

static PyObject*
board2Code(PyObject*, PyObject* args)
{
  PyObject* pyBoard;
  
  if( !PyArg_ParseTuple(args, "O", &pyBoard) ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }

  if( !(PySequence_Check(pyBoard) && PySequence_Size(pyBoard) == 22) ) {
    PyErr_SetString(PyExc_ValueError, "wrong args.");
    return 0;
  }

  int board[22];
  {
    PyObject** s = &PyList_GET_ITEM(pyBoard, 0);
    for(uint k = 0; k < 22; ++k) {
      board[k] = PyInt_AsLong(s[k]);
    }
  }

  bool s[31] = {false};
  
  uint o = 0;
  for(uint k = 0; k < 14; ++k) {
    o += board[k] == 1;
  }

  uint const totPiecesMe = 7 - board[GR_OFF];
  uint const atHome = totPiecesMe - o;

  uint k = 0;
  s[k] = atHome & 0x4; ++k;
  s[k] = atHome & 0x2; ++k;
  s[k] = atHome & 0x1; ++k;
  for(uint i = 0; i < 4; ++i) {
    s[k] = board[i]; ++k;
  }
  for(uint i = 12; i < 14; ++i) {
    s[k] = board[i]; ++k;
  }

  uint oo = 0;
  for(uint k = 15; k < 19; ++k) {
    oo += board[k] == -1;
  }
  for(uint k = 4; k < 12; ++k) {
    oo += board[k] == -1;
  }
  for(uint k = 19; k < 21; ++k) {
    oo += board[k] == -1;
  }

  uint const ototPiecesOff = 7 - board[RD_OFF];
  uint const oatHome = ototPiecesOff - oo;

  s[k] = oatHome & 0x4; ++k;
  s[k] = oatHome & 0x2; ++k;
  s[k] = oatHome & 0x1; ++k;
  for(uint i = 15; i < 19; ++i) {
    s[k] = board[i]; ++k;
  }
  for(uint i = 19; i < 21; ++i) {
    s[k] = board[i]; ++k;
  }
  
  uint x = board[4] + 1;
  for(uint i = 5; i < 12; ++i) {
    x = 3*x + (board[i] + 1);
  }
  for(int i = 12; i >= 0; --i) {
    s[k] = x & (0x1 << i); ++k;
  }

  char a[5];
  b2a(s, a);
  return PyString_FromStringAndSize(a, 5);
}

static PyMethodDef irMethods[] =
{
  {"board2Index", board2Index, METH_VARARGS, ""},
  
  {"index2Board", index2Board, METH_VARARGS, ""},

  {"code2Board",  code2Board, METH_VARARGS, ""},

  {"board2Code",  board2Code, METH_VARARGS, ""},
  
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initirogaur(void)
{
  initm();
  /*PyObject* m = */ Py_InitModule("irogaur", irMethods);
}

