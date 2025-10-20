-- 用户表：存储所有用户的基本信息
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nickname VARCHAR(50) NOT NULL COMMENT '用户昵称',
    identity ENUM('teacher', 'parent') NOT NULL COMMENT '用户身份：老师或家长',
    email VARCHAR(100) UNIQUE COMMENT '电子邮箱',
    phone VARCHAR(20) UNIQUE NOT NULL COMMENT '手机号码，用于登录',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    avatar_url VARCHAR(255) COMMENT '头像URL',
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active' COMMENT '账号状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_identity (identity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户基本信息表';

-- 认证令牌表：管理access_token及刷新机制
CREATE TABLE auth_tokens (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '关联的用户ID',
    access_token VARCHAR(255) NOT NULL COMMENT '访问令牌',
    refresh_token VARCHAR(255) NOT NULL COMMENT '刷新令牌',
    expires_at TIMESTAMP NOT NULL COMMENT '令牌过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE INDEX idx_access_token (access_token),
    UNIQUE INDEX idx_refresh_token (refresh_token),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户认证令牌表';

-- 老师信息表：存储教师特有信息
CREATE TABLE teachers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL UNIQUE COMMENT '关联的用户ID',
    subject VARCHAR(100) NOT NULL COMMENT '教授科目，多个用逗号分隔',
    education VARCHAR(50) COMMENT '学历',
    experience TEXT COMMENT '教学经验',
    introduction TEXT COMMENT '个人介绍',
    hourly_rate DECIMAL(10, 2) NOT NULL COMMENT '时薪',
    rating DECIMAL(3, 2) DEFAULT 0 COMMENT '平均评分',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_subject (subject)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='教师信息表';

-- 家长信息表：存储家长特有信息
CREATE TABLE parents (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL UNIQUE COMMENT '关联的用户ID',
    child_grade VARCHAR(50) COMMENT '孩子年级',
    needs TEXT COMMENT '家教需求描述',
    hourly_rate DECIMAL(10, 2) NOT NULL COMMENT '时薪',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='家长信息表';

-- 后续可根据业务扩展以下表：
-- 1. 课程表（courses）- 存储课程信息
-- 2. 订单表（orders）- 存储交易订单
-- 3. 评价表（reviews）- 存储用户评价
-- 4. 消息表（messages）- 存储用户间沟通消息
