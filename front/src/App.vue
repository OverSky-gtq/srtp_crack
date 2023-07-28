<template>
    <div class="wrapper">
        <el-tabs v-model="activeName" type="card" class="demo-tabs" @tab-click="handleClick">
            <el-tab-pane label="图片配准" name="first"></el-tab-pane>
            <el-tab-pane label="裂缝识别" name="second"></el-tab-pane>
        </el-tabs>
        <router-view />
    </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import type { TabsPaneContext } from "element-plus";
import { useRouter } from "vue-router";

const activeName = ref("first");
const router = useRouter();

const handleClick = (pane: TabsPaneContext, event: Event) => {
    // Get the name of the selected tab
    const selectedTabName = pane.paneName;

    // Define the routes corresponding to each tab
    const routeMappings = {
        first: "/image",
        second: "/crack",
    };

    // Use the router.push() method to navigate to the corresponding route
    router.push(routeMappings[selectedTabName]);
};
</script>

<style>
.demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}
</style>
