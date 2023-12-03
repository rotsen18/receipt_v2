import ReceiptList from "@/components/ReceiptList.vue";
import ReceiptDetail from "@/components/ReceiptDetail.vue";

const routes = [
  { path: "/receipts", component: ReceiptList },
  { path: "/receipts/:id", name: "receipt-detail", component: ReceiptDetail }
];

export default routes;
