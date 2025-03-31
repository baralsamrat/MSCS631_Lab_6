 # MSCS631_Lab_6
Samrat Baral

Lab 6

University of the Cumberlands

2025 Spring - Advanced Computer Networks (MSCS-631-M40) - Full Term
Dr. Yousef Nijim

March 30, 2025

implement a traceroute application using ICMP request and reply to messages
# Screenshot
![1](/screeenshots/Capture-1.png)
![2](/screeenshots/Capture-2.png)
![3](screeenshots/Capture-3.png)

# Ouput 
```bash
chmod +x main.sh
```

```bash
./main.sh

```
# Experience and Challenges:
- Working on this proxy server lab was a valuable exercise in understanding the fundamentals of network programming and HTTP. I appreciated how the lab required me to handle both caching and live HTTP requests. Implementing the caching mechanism provided insight into how web content can be stored and reused, reducing unnecessary traffic and latency. It was interesting to see the interplay between the client’s request and the server’s response, and to learn how even a simple proxy can play a critical role in network performance and efficiency.

- One of the main challenges I faced was managing the intricacies of socket communication, especially in dealing with the blocking behavior of socket calls and ensuring that data was correctly read and forwarded in chunks. Handling different types of content (text versus binary) also presented a challenge, as the basic implementation is more suited to HTML files than images or other media. These obstacles underscored the importance of robust error handling and thoughtful design when building networked applications—a valuable lesson for any developer working in the field of network programming.
