FROM ubuntu:22.04@sha256:b4b521bfcec90b11d2869e00fe1f2380c21cbfcd799ee35df8bd7ac09e6f63ea as chroot

COPY flag.txt /flag.txt
COPY ponmap /ponmap

FROM disconnect3d/nsjail:3.1-6483728

COPY --from=chroot / /chroot

CMD ["nsjail", "-Ml", "--port", "3337", "--user", "99999", "--group", "99999", "--disable_proc", "--chroot", "/chroot/", "/ponmap"]
