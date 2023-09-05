"""
rtcmpoller.py

This example illustrates how to read and display RTCM messages
"concurrently" with other tasks using threads and queues. This
represents a useful generic pattern for many end user applications.

It implements two threads which run concurrently:
1) an I/O thread which continuously reads RTCM data from the
receiver and sends any queued outbound command or poll messages.
2) a process thread which processes parsed RTCM data - in this example
it simply prints the parsed data to the terminal.
RTCN data is passed between threads using queues.

Press CTRL-C to terminate.

FYI: Since Python implements a Global Interpreter Lock (GIL),
threads are not strictly concurrent, though this is of minor
practical consequence here.

Created on 07 Aug 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

from queue import Queue
from sys import platform
from threading import Event, Lock, Thread
from time import sleep
from serial import Serial
from pyrtcm import RTCMReader


def io_data(
    stream: object,
    rtr: RTCMReader,
    readqueue: Queue,
    sendqueue: Queue,
    stop: Event,
):
    """
    THREADED
    Read and parse inbound RTCM data and place
    raw and parsed data on queue.

    Send any queued outbound messages to receiver.
    """
    # pylint: disable=broad-exception-caught

    while not stop.is_set():
        if stream.in_waiting:
            try:
                (raw_data, parsed_data) = rtr.read()
                if parsed_data:
                    readqueue.put((raw_data, parsed_data))

                # refine this if outbound message rates exceed inbound
                while not sendqueue.empty():
                    data = sendqueue.get(False)
                    if data is not None:
                        rtr.datastream.write(data.serialize())
                    sendqueue.task_done()

            except Exception as err:
                print(f"\n\nSomething went wrong {err}\n\n")
                continue


def process_data(queue: Queue, stop: Event):
    """
    THREADED
    Get RTCM data from queue and display.
    """

    while not stop.is_set():
        if queue.empty() is False:
            (_, parsed) = queue.get()
            print(parsed)
            queue.task_done()


if __name__ == "__main__":
    # set port, baudrate and timeout to suit your device configuration
    if platform == "win32":  # Windows
        port = "COM13"
    elif platform == "darwin":  # MacOS
        port = "/dev/tty.usbmodem101"
    else:  # Linux
        port = "/dev/ttyACM1"
    baudrate = 38400
    timeout = 0.1

    DELAY = 1

    with Serial(port, baudrate, timeout=timeout) as serial_stream:
        ubxreader = RTCMReader(serial_stream)

        serial_lock = Lock()
        read_queue = Queue()
        send_queue = Queue()
        stop_event = Event()

        io_thread = Thread(
            target=io_data,
            args=(
                serial_stream,
                ubxreader,
                read_queue,
                send_queue,
                stop_event,
            ),
        )
        process_thread = Thread(
            target=process_data,
            args=(
                read_queue,
                stop_event,
            ),
        )

        print("\nStarting handler threads. Press Ctrl-C to terminate...")
        io_thread.start()
        process_thread.start()

        # loop until user presses Ctrl-C
        while not stop_event.is_set():
            try:
                # DO STUFF IN THE BACKGROUND...
                sleep(20)
                stop_event.set()
            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        io_thread.join()
        process_thread.join()
        print("\nProcessing complete")
