FROM ubuntu:26.04@sha256:91832dcd7bc5e44c098ecefc0a251a5c5d596dae494b33fb248e01b6840f8ce0 AS chroot

COPY app /
RUN mv /flag.txt /flag-$(md5sum /flag.txt | awk '{print $1}').txt

FROM ghcr.io/google/nsjail/nsjail@sha256:03a904cd42b07ecc6e6f318c1ea14bd28339e1411d180d8744b2a5e2929e895f

COPY --from=chroot / /chroot
COPY nsjail.cfg /nsjail.cfg

CMD ["nsjail", "--config", "/nsjail.cfg"]