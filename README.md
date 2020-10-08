# Readme

## How to use the app

The project is written in docker and requires building as part of its initial setup. The project
uses the Nameko framework which requires RabbitMQ to be installed.

### Building

Issue the command `docker build -t assignment .` in the root of the repository to build the docker
image.

### Running

Issue the command  `docker run --rm --name dev_assignment -p 8000:8000 -it assignment`.

#### Configuration

The service can be configured with the following environment variables:

* **RABBITMQ_USER**
  * The user to login to the rabbitmq host with.
  * Default: guest
* **RABBITMQ_PASSWORD**
  * The password to login to the rabbitmq host with.
  * Default: guest
* **RABBITMQ_HOST**
  * The location of the rabbitmq cluster that serves the service.
  * Default: localhost
* **WORDS_PATH**
  * The location of the words frequency file. A default is included in the words file in the root
  directory.
  * Default: words
* **LOG_LEVEL**
  * The log level that the service is ran at.
  * Default: DEBUG

## Retrospective

I thought the task was straight-forward. Aside from a few complications with autoreloading the
nameko runner and a few questions about task 2 and 3 it proceeded smoothly.

### Thoughts

Task 1 was very simple. I coded it first and used that to get my development environment to my
liking. The coding of task 1 took less than 5 minutes and no real problems were encountered.
Researching Nameko and seeing what it had to offer took approximately 30 minutes. I found Nameko's
documentation a bit on the light side when it comes to examples and best practices. I ended having
to read code on how other people were doing things to find out certain things.

I spent an addition 1 hour and 30 minutes setting up my Dockerfile and getting a development cycle
setup. I prefer my development cycle to have autoreloading of the service and this is not possible
with standard Nameko. I ran into a project called nameko-dev[https://pypi.org/project/nameko-dev/]
which claimed to do autoreloading, but was completely unable to get that to occur. It also had no
documentation available. Eventually I ditched nameko-dev and crafted a command using watchexec.
watchexec is a Rust project and is available here [https://crates.io/crates/watchexec]. The command
that I used was:

```bash
docker run --rm --name dev_assignment <...docker run cmd>;
watchexec -p -d 0 -w src -w config.yaml "docker restart dev_assignment; echo 'restarting';"
```

This greatly improved local developer experience, but was still pretty brittle as Python syntax
errors can cause the container to stop. I decided I had done enough though and moved on to task 2
and task 3.

Task 2 and 3 were similar in that they both relate to Huffman compression so I decided that it
should be seperated for cleanliness. We did Huffman compression at UCT and I have coded it before so
I have some in-depth knowledge of the subject. The first thing I did is find a Huffman encoding
package on PyPi. I found the Huffman package within a few minutes of searching
[https://pypi.org/project/huffman/]. Initially, I thought it would do everything for me but after
some digging into the code I realised it didn't, it only created the codebooks from a given set of
frequencies. I decided to use the package as the encoding and decoding part of Huffman encoding are
the easy bits and codebook generation is the harder bit.

I also realized at this point that the tasks were underconstrained. To properly decode a string in
Huffman encoding you need the codebook that you originally used to encode it. If you don't have that
the decoding sequence is ambiguous. Since codebooks weren't mentioned in the assignment, I decided
that the service would have its own static codebook that it made on startup. The frequencies for
this would come from a list of words instead of just a hardcoded frequency table as it made testing
the service easier, the word list could come from /usr/share/dict/words which is available on any
Linux machine. All in all task 2 and task 3 took about 30 minutes to code up.

I spent an additional hour polishing everything up and making sure there were comments and a
small amount of testing was done.

Finally, I wrote up this README file which took approximately an hour. In the end, the entire task
took between 4 and 5 hours to do.

The biggest problem I found was the lack of autoreloading in Nameko but I managed to work around it.
