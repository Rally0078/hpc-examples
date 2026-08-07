To use SSH tunneling to access Dask dashboard

```bash
ssh -N -L 8787:nodeX:8787 username@hpc-login-addr.net
```
Replace X with the appropriate node number, username and hpc login with the correct details

To compile C

```sh
mpicc ./ompi_c/main.c -o ./ompi_c/a.out -cc=gcc
```

To compile Fortran90

```sh
mpif90 ./ompi_f/main.f90 -o ./ompi_f/a.out
```