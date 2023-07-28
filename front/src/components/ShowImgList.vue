<template>
    <div class="demo-image__preview">
        <el-image
                style="width: 300px; height: 300px"
                :src="url"
                :zoom-rate="1.2"
                :preview-src-list="srcList"
                :initial-index="4"
                fit="cover"
        />
    </div>
</template>

<script  setup>
defineProps(['srcList',])
const url =
    'https://img1.imgtp.com/2023/07/28/WjybdjLU.png'
</script>

<style scoped>
.demo-image__error .image-slot {
    font-size: 30px;
}
.demo-image__error .image-slot .el-icon {
    font-size: 30px;
}
.demo-image__error .el-image {
    width: 100%;
    height: 200px;
}
</style>
