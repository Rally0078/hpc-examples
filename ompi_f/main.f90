program main
    use mpi
    integer process_rank, cluster_size, ierror
    call MPI_INIT(ierror)
    call MPI_COMM_SIZE(MPI_COMM_WORLD, cluster_size, ierror)
    call MPI_COMM_RANK(MPI_COMM_WORLD, process_rank, ierror)

    print *, "Hello world in Fortran90 from Process", process_rank, ' of ', cluster_size

    call MPI_FINALIZE(ierror)
end program