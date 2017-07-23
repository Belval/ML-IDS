# ML-IDS
Applying machine learning principles to the information security field through intelligent intrusion detection systems.

This is a three phases project that can roughly described as

- Data gathering
- Model developpement
- Hardware implementation

## Data gathering

There are a few freely available datasets that applies to the field, I could attempt to create my own set by setting up a virtual machine exposed to the Internet but it is unlikely that I will record any privilege escalation attack (or any sophisticated attacks really) only DoS, DDoS, SSH bruteforce and scans could really be recorded.

### Freely available datasets

- [DARPA Intrusion Detection Data Sets](https://www.ll.mit.edu/ideval/data/) (1998-2000)
- [KDD Cup](https://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html) (1999)

### Not freely available datasets

- [UNB ICX IDS 2012](http://www.unb.ca/cic/research/datasets/ids.html) (Request sent)

For the first part of the prototyping process, the KDD Cup dataset will be used as it was preprocessed already.

## Model developpement

While researchers already explored most machine model, they forgot one aspect that is crucial to the project at hand: resources. The whole point being to end up with a usable hardware implementation, it is impossible to afford more than a few milliseconds for each packets on a rather weak machine. I will refrain from going straight to the LSTM and take the time to benchmark the performance of other well-known algorithms. I will explore three models to identify the one that shows the best performance to resources among logistic regression, support-vector machines, deep feedforward neural networks, and LSTM recurrent networks.

To avoid reinventing the basics, I will use the TensorFlow framework that supports both x86-64 and ARM.

### Logistic regression

- Pros
    - Fast inference
    - Simple to understand because it is not a blackbox
- Cons
    - Probably too simple to correctly fit the problem
    - No conception of time

### Support Vector Machines
- Pros
    - Usable for semi-supervised learning if using TSVM (unlabelled data)
    - It finds the global minimum
- Cons
    - A normal SVM will not return a prediction confidence and it's a big handicap in later implementation.
    - No conception of time

### Standard FeedForward Neural Network
- Pros
    - Complex enough to fit most problem
- Cons
    - No conception of time

### LSTM Recurrent Neural Network
- Pros
    - Works with sequence, in our case, the packet that came before could be related to the next one. Such relation wouldn't be handled by the above models.
    - Documented use in IDS
- Cons
    - More complex than all three of the above.

## Hardware implementation

### Training

I will use my personnal computer for the training, if someone wishes to replicate the process, AWS offers VPS with GPUs []().

- AMD Zen 1700
- Nvidia GTX 1080Ti

### Inference

These are merely supposition on what minimal hardware would be required based on the platform. In the case at end I will use an x86-64 processor because the cost for a dual gigabit port is lower and the hardware will be supported out of the box (I'd rather avoid troubleshooting hardware issues).

- x86-64
    - 2 cores celeron processor (would scale if more processing power was available)
- ARM
    - 4 cores ARMv8 or more recent
- 2-4 GB RAM

For portability and performance, the inference will be done in C++.

## References

All consulted papers & documentation is available in the "papers" folder.