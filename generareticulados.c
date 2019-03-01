int
FindMax (i)
{
  int k = 0;
  int j, s, a;
  for (j = 0; j < i; j++)
    {
      s = 1;
      for (a = 0; a < i; a++)
	if (a != j && J[a][j] == a)
	  s = 0;
      if (s)
	{
	  M[k] = j;
	  k++;
	}
    }
  a = rnd (k);
  a++;
  for (j = 0; j < k; j++)
    Q[j] = 0;
  for (s = 0; s < a; s++)
    {
      j = rnd (k);
      if (Q[j])
	s--;
      else
	Q[j] = 1;
    }
  return k;
}

void
Work (i)
{
  int j, l, w, s, q, u;
  if (i == N - 1)
    {
      for (j = 0; j < N; j++)
	for (l = 0; l < N; l++)
	  if (J[j][l] == -1)
	    J[j][l] = N - 1;
      return;
    }
  q = S[N - i]
  if (i == 1)
    {
      u = 1;
      M[0] = 0;
      Q[0] = 1;
    }
  else if (!rnd (q))
    u = FindMax (i);
  for (j = 0; j < u; j++)
    if (Q[j])
      {
	J[M[j]][i] = i;
	J[i][M[j]] = i;
      }
  w = 1;
  while (w)
    {
      w = 0;
      for (j = 0; j < i; j++)
	if (J[j][i] == i)
	  for (s = 0; s < i; s++)
	    if (J[s][j] == j && J[s][i] != i)
	      {
		w = 1;
		J[s][i] = i;
		J[i][s] = i;
	      }
      for (j = 0; j < i; j++)
	if (J[j][i] == i)
	  for (l = 0; l < i; l++)
	    if (J[l][i] == i)
	      {
		s = J[j][l];
		if (s != -1 && J[s][i] != i)
		  {
		    w = 1;
		    J[s][i] = i;
		    J[i][s] = i;
		  }
	      }
    }
  for (j = 0; j < i; j++)
    if (J[j][i] == i)
      for (l = 0; l < i; l++)
	if (J[l][i] == i && J[j][l] == -1)
	  {
	    J[j][l] = i;
	    J[l][j] = i;
	  }
}

void main(){
    printf("%s",Work(0))
}
