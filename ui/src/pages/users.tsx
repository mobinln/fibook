import DataTable from "@/components/DataTable";

export default function Users() {
  return (
    <div className="container mx-auto">
      <DataTable
        url="/users"
        columns={[
          { name: "email", header: "Email" },
          { name: "full_name", header: "Full Name" },
          { name: "is_active", header: "Is Active" },
          { name: "is_superuser", header: "Is Super User" },
        ]}
      />
    </div>
  );
}
