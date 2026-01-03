import socket
import threading

def receive_messages(client):
    """接收服务器消息的线程函数"""
    while True:
        try:
            data, addr = client.recvfrom(1024)
            print(f"服务器消息: {data.decode()}")
        except Exception as e:
            print(f"接收消息出错: {e}")
            break

def main():
    # 创建UDP客户端
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host=input("请输入服务器IP地址 ")
    server_addr = (host, 3729)
    
    # 注册为hacker
    client.sendto('hacker'.encode(), server_addr)
    print("您已注册为Hacker，可以发送指令给User")
    
    # 创建接收消息的线程
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()
    
    try:
        # Hacker输入指令发送给User
        while True:
            print("\n请选择发送方式：")
            print("1. 广播（发送给所有User）")
            print("2. 定向发送（发送给特定User）")
            print("3. 退出程序")
            
            choice = input("请输入选择 (1/2/3): ")
            
            if choice == '1':
                # 广播消息
                command = input("请输入要广播的指令: ")
                if command:
                    client.sendto(command.encode(), server_addr)
            elif choice == '2':
                # 定向发送
                user_id = input("请输入目标User ID (例如: user0): ")
                if not user_id:
                    print("User ID不能为空")
                    continue
                command = input("请输入要发送的指令: ")
                if command:
                    # 格式：user_id:message
                    client.sendto(f"{user_id}:{command}".encode(), server_addr)
            elif choice == '3':
                # 退出程序
                break
            else:
                print("无效的选择，请重新输入")
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
        print("客户端已关闭")

if __name__ == "__main__":
    main()