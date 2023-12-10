import HelloWorld from "@/components/HelloWorld.vue";
import ReceiptList from "@/components/ReceiptList.vue";
import ReceiptDetail from "@/components/ReceiptDetail.vue";

const routes = [
    { path: "/", name: "home", component: HelloWorld },
    { path: "/receipts", name: "receipt-list", component: ReceiptList },
    { path: "/receipts/:id", name: "receipt-detail", component: ReceiptDetail }
];

export default routes;
