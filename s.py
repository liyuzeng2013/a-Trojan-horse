import socket
import threading

sever = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_list = ('localhost', 3729)
user_list = {}
# 分离hacker和user列表以便管理
hackers = {}
users = {}
sever.bind(host_list)

# 处理客户端请求的函数
def handle_client(data, addr):
    print(f"{addr}: {data.decode()}")
    message = data.decode()
    
    # 判断是否是身份标识消息
    if message == 'hacker':
        # 添加到hacker列表
        hacker_id = f"hacker{len(hackers)}"
        hackers[hacker_id] = addr
        user_list[hacker_id] = addr  # 同时保留在总列表中
        sever.sendto(f"您已成功注册为{hacker_id}".encode(), addr)
        # 发送当前用户列表给新注册的hacker
        sever.sendto(f"当前用户列表: {str(users)}".encode(), addr)
    elif message == 'user':
        # 添加到user列表
        user_id = f"user{len(users)}"
        users[user_id] = addr
        user_list[user_id] = addr  # 同时保留在总列表中
        sever.sendto(f"您已成功注册为{user_id}".encode(), addr)
    else:
        # 判断发送者是否为hacker
        is_hacker = False
        hacker_id = None
        for hid, haddr in hackers.items():
            if haddr == addr:
                is_hacker = True
                hacker_id = hid
                break
        
        if is_hacker:
            # 解析消息格式，判断是广播还是定向发送
            if ':' in message:
                # 定向发送格式：user_id:message
                target_user, content = message.split(':', 1)
                if target_user in users:
                    # 向特定user发送消息
                    user_addr = users[target_user]
                    sever.sendto(f"{content}".encode(), user_addr)
                    print(f"hacker{hacker_id}向{target_user}发送了指令: {content}")
                    # 向hacker确认消息已发送
                    sever.sendto(f"指令已发送给{target_user}".encode(), addr)
                else:
                    # 用户不存在
                    sever.sendto(f"用户{target_user}不存在".encode(), addr)
            else:
                # 广播消息给所有user
                print(f"hacker{hacker_id}广播指令: {message}")
                for user_id, user_addr in users.items():
                    sever.sendto(f"{message}".encode(), user_addr)
                # 向hacker确认消息已广播
                sever.sendto(f"指令已广播给所有用户".encode(), addr)
        else:
            # 普通消息处理
            sever.sendto("未知消息类型".encode(), addr)

print("服务器已启动，等待客户端连接...")
while True:
    try:
        data, addr = sever.recvfrom(1024)
        # 为每个客户端请求创建一个新线程
        client_thread = threading.Thread(target=handle_client, args=(data, addr))
        client_thread.daemon = True  # 设置为守护线程，主程序结束时自动退出
        client_thread.start()
    except KeyboardInterrupt:
        print("服务器已关闭")
        break

sever.close()