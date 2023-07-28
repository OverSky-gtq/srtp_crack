<template>
    <div class="demo-image">
        <div key='contain' class="block">
            <el-image style="min-width: 750px; max-height: 1000px" :src="url" fit='contain'/>
        </div>
    </div>
</template>

<script setup>
defineProps(['url'])
</script>

<style scoped>
.demo-image .block {
    padding: 30px 0;
    text-align: center;
    border-right: solid 1px var(--el-border-color);
    display: inline-block;
    width: 20%;
    box-sizing: border-box;
    vertical-align: top;
}
.demo-image .block:last-child {
    border-right: none;
}
</style>
