# Surgical Instrument Tracking System 

## The Problem it Solved

Last semester, one of our team members visited Johns Hopkins Medical School where he was able to shadow open-heart surgeries. He was shocked to see surgeons occasionally mistakenly leave equipment inside patients, and even more aghast to learn that this was not an uncommon issue. In fact, last year alone there were 75000 instances of patients retaining equipment post-surgery.

Our team designed Surgical Eye to tackle the challenge of retaining surgical items (RSI) by utilizing object tracking algorithms to identify and monitor surgical tools during procedures. With over 200 tools commonly used by surgeons and thousands of retained surgical item (RSI) cases reported annually, keeping track of surgical instruments is essential for both safety and management purposes. Surgical Eye provides a solution by leveraging transfer learning to create a customized model for identifying surgical tools in real-time. By accurately tracking these tools throughout the surgical process, Surgical Eye helps reduce the risk of RSI cases and enhances patient safety in the operating room.

## Challenges We Ran Into

Fine-tuning a model specifically tailored for surgeon tools: Developing a model that accurately identifies surgical tools required extensive fine-tuning and customization. We faced challenges in optimizing the model's performance and ensuring robustness across various surgical settings. To overcome this hurdle, we conducted thorough experimentation and parameter tuning, leveraging transfer learning techniques and domain-specific knowledge to enhance the model's accuracy.

Integrating a full-stack application with the Taipy library: Integrating the object tracking model with a full-stack application posed challenges in terms of compatibility and API integration. We encountered difficulties in synchronizing data between the front-end interface and the back-end server, as well as in managing real-time updates from the object tracking algorithm. To address this, we reduced the number of frames the object tracking model was used on, thereby increasing frame rate.

Limited documentation for generative AI applications: Exploring generative AI techniques for object tracking and identification presented challenges due to the limited documentation and resources available. We encountered difficulties in understanding and implementing advanced generative models for object localization and tracking. To overcome this obstacle, we pivoted our generative ai efforts to focus on creating a text-based description of the video and consulted domain experts, such as the Archetype AI developers.

## Technologies We Used
* PyTorch
* OpenCV
* Archetype AI
* Google Colab
* Numpy
* Ultralytics
* TaiPy
* Flask
* Selenium

## License 

Distributed under the MIT License. See `LICENSE` for more information.

## Team Members

- Kunal Aneja
- Shlok Dholakia
- Rishi Aniga
- Lucas Zhang
