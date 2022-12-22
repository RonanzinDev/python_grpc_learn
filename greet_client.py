import greet_pb2_grpc
import greet_pb2
import time
import grpc

def get_client_stream_requests():
    while True:
        name = input("Plese enter a name(or nothin to stop the server): ")
        if name == "":
            break
        
        hello_request = greet_pb2.HelloRequest(greeting = "Hello", name = name)
        yield hello_request
        time.sleep(1)

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. Say Hello - Unary")
        print("2. ParrotSayHello - ServerSide Streaming")
        print("3. ChattyClientSaysHello- Client Side Streaming")
        print("4. InteractingHello - Both streaming")
        rpc_call = input("Which rpc would u like to call: ")
        if rpc_call ==  "1":
            hello_request = greet_pb2.HelloRequest(greeting = "Hello World", name = "Gabriel")
            hello_reply = stub.SayHello(hello_request)
            print("SayHello response received")
            print(hello_reply)
        
        elif rpc_call ==  "2":
            hello_request = greet_pb2.HelloRequest(greeting = "Hello World", name = "Gabriel")
            hello_replies = stub.ParrotSaysHello(hello_request)
            for hello_reply in hello_replies:  
                print("ParrotSayHello response received")
                print(hello_reply)
                
        elif rpc_call ==  "3":
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_requests())    
            print("ChattyClientSaysHello Response Received")
            print(delayed_reply)
        elif rpc_call ==  "4":
            responses = stub.InteractingHello(get_client_stream_requests())
            for response in responses:
                print("InteractingHello Response was received: ")
                print(response)
            
            
            
if __name__ == "__main__":
    run()