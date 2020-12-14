f = open("test_y", "w") with torch.no_grad():
    for i, (images, labels) in enumerate(test_loader, 0):
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        file = os.listdir(TEST_DATA_PATH + "/all")[i] format = file + ", " + str(predicted.item()) + '\n'
        f.write(format)
        f.close()