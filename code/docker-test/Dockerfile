FROM alpine:3.8
ENV TERRAFORM_VERSION 0.12.13
ENV ANSIBLE_VERSION 2.6.3

RUN apk add --update wget ca-certificates unzip python py-pip openssl bash && \
    apk --update add openssh-client && \
    apk --update add --virtual build-dependencies python-dev libffi-dev openssl-dev build-base && \
    apk add --virtual=build gcc libffi-dev musl-dev && \
    python -m pip install --upgrade pip && \
    # pip install azure-cli && \
    pip install --upgrade pip cffi && \
    pip install ansible==${ANSIBLE_VERSION} && \
    wget -q -O /terraform.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" && \
    unzip /terraform.zip -d /bin && \
    apk del build-dependencies && \
    rm -rf /var/cache/apk/* /terraform.zip
ENTRYPOINT ["bash"]
