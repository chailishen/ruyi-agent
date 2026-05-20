"use client";

import { isMockMode } from "@/mocks/config";
import { createMockJwt } from "@/mocks/auth/tokens";
import { storeLoginToken } from "@/utils/cookieUtils";
import { useQueryClient } from "@tanstack/react-query";
import { Select, Tag } from "antd";
import { useState } from "react";

const ROLES = [
  { value: "proxy_admin", label: "Admin" },
  { value: "proxy_admin_viewer", label: "Admin Viewer" },
  { value: "internal_user", label: "Internal User" },
];

export default function MockRoleSwitcher() {
  const queryClient = useQueryClient();
  const [role, setRole] = useState("proxy_admin");

  if (!isMockMode()) {
    return null;
  }

  return (
    <div className="flex items-center gap-2">
      <Tag color="gold">Prototype</Tag>
      <Select
        size="small"
        value={role}
        options={ROLES}
        style={{ width: 140 }}
        onChange={(value) => {
          setRole(value);
          storeLoginToken(createMockJwt(value));
          queryClient.clear();
          window.location.reload();
        }}
      />
    </div>
  );
}
